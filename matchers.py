import re
from abc import ABC, abstractmethod

class ILineMatcher(ABC):
    @abstractmethod
    def match(self, line: str) -> bool:
        pass

class ExactMatcher(ILineMatcher):
    def __init__(self, keyword: str, ignore_case: bool = False):
        self.ignore_case = ignore_case
        self.keyword = keyword.lower() if ignore_case else keyword

    def match(self, line: str) -> bool:
        target = line.lower() if self.ignore_case else line
        return self.keyword in target

class RegexMatcher(ILineMatcher):
    def __init__(self, pattern: str, ignore_case: bool = False):
        flags = re.IGNORECASE if ignore_case else 0
        self.regex = re.compile(pattern, flags)

    def match(self, line: str) -> bool:
        return bool(self.regex.search(line))