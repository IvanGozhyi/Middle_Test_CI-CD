import re
from abc import ABC, abstractmethod

class ILineMatcher(ABC):
    @abstractmethod
    def match(self, line: str) -> bool:
        pass