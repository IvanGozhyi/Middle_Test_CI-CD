import pytest
from pathlib import Path
from matchers import ExactMatcher, RegexMatcher
from processor import FileProcessor


@pytest.fixture
def sample_text_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "test_input.txt"
    content = (
        "Error: connection lost\n"
        "Warning: low memory\n"
        "Info: system started\n"
        "error: disk full\n"
        "123 critical failure"
    )
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def output_file_path(tmp_path: Path) -> Path:
    return tmp_path / "test_output.txt"


@pytest.mark.parametrize("keyword, ignore_case, line, expected", [
    ("Error", False, "Error: connection lost", True),
    ("Error", False, "error: disk full", False),
    ("Error", True, "error: disk full", True),
    ("Info", False, "Warning: low memory", False),
])
def test_exact_matcher(keyword, ignore_case, line, expected):
    matcher = ExactMatcher(keyword, ignore_case)
    assert matcher.match(line) == expected


@pytest.mark.parametrize("pattern, ignore_case, line, expected", [
    (r"^\d+", False, "123 critical failure", True),
    (r"^\d+", False, "Error 123", False),
    (r"warning|error", True, "Warning: low memory", True),
    (r"warning|error", False, "Warning: low memory", False),
])
def test_regex_matcher(pattern, ignore_case, line, expected):
    matcher = RegexMatcher(pattern, ignore_case)
    assert matcher.match(line) == expected


def test_file_processor_logic(sample_text_file, output_file_path):
    matcher = ExactMatcher("error", ignore_case=True)
    processor = FileProcessor(sample_text_file, output_file_path, matcher)

    total_lines, found_lines = processor.process()

    assert total_lines == 5
    assert found_lines == 2

    output_content = output_file_path.read_text(encoding="utf-8")
    assert "Error: connection lost\n" in output_content
    assert "error: disk full" in output_content
    assert "Warning" not in output_content