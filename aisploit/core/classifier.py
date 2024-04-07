from abc import ABC, abstractmethod
from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    flagged: bool
    score_type: Literal["int", "float", "str", "bool"]
    score_value: int | float | str | bool
    score_description: str = ""
    score_explanation: str = ""


class BaseClassifier(ABC):
    @abstractmethod
    def score_text(self, text: str) -> Score:
        """Score the text and return a Score object."""
        raise NotImplementedError("score_text method not implemented")
