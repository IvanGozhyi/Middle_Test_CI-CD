from pathlib import Path
from matchers import ILineMatcher

class FileProcessor:
    def __init__(self, input_path: Path, output_path: Path, matcher: ILineMatcher):
        self.input_path = input_path
        self.output_path = output_path
        self.matcher = matcher

    def process(self) -> tuple[int, int]:
        total_lines = 0
        lines_found = 0

        with self.input_path.open('r', encoding='utf-8') as infile, \
                self.output_path.open('w', encoding='utf-8') as outfile:

            for line in infile:
                total_lines += 1
                if self.matcher.match(line):
                    outfile.write(line)
                    lines_found += 1

        return total_lines, lines_found