from pathlib import Path
from matchers import ILineMatcher

class FileProcessor:
    def __init__(self, input_path: Path, output_path: Path, matcher: ILineMatcher):
        self.input_path = input_path
        self.output_path = output_path
        self.matcher = matcher