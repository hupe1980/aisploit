from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass

T = TypeVar("T")
Input = TypeVar("Input")


@dataclass(frozen=True)
class Score(Generic[T]):
    """A class representing a score.

    Attributes:
        flagged (bool): Whether the score is flagged.
        value (T): The value of the score.
        description (str): Optional description of the score.
        explanation (str): Optional explanation of the score.
    """

    flagged: bool
    value: T
    description: str = ""
    explanation: str = ""


class BaseClassifier(ABC, Generic[T, Input]):
    """An abstract base class for classifiers."""

    @abstractmethod
    def score(self, input: Input) -> Score[T]:
        """Score the input and return a Score object.

        Args:
            input (Input): The input to be scored.

        Returns:
            Score[T]: A Score object representing the score of the input.
        """
        pass


class BaseTextClassifier(BaseClassifier[T, str], Generic[T]):
    """An abstract base class for text classifiers."""

    pass
