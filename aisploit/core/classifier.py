from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass


T = TypeVar("T")


@dataclass(frozen=True)
class Score(Generic[T]):
    """A class representing a score."""

    flagged: bool
    value: T
    description: str = ""
    explanation: str = ""


class BaseClassifier(ABC, Generic[T]):
    """An abstract base class for classifiers."""

    @abstractmethod
    def score_text(self, text: str) -> Score[T]:
        """Score the text and return a Score object.

        Args:
            text (str): The text to be scored.

        Returns:
            Score[T]: A Score object representing the score of the text.
        """
        pass
