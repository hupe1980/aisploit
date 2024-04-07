from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass


T = TypeVar("T", int, float, str, bool)


@dataclass(frozen=True)
class Score(Generic[T]):
    flagged: bool
    value: T
    description: str = ""
    explanation: str = ""


class BaseClassifier(ABC, Generic[T]):
    @abstractmethod
    def score_text(self, text: str) -> Score[T]:
        """Score the text and return a Score object."""
        pass
