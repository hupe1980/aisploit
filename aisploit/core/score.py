from abc import ABC, abstractmethod
from typing import Literal
from dataclasses import dataclass


@dataclass
class Score:
    score_type: Literal["int", "float", "str", "bool"]
    score_value: int | float | str | bool
    score_description: str = ""
    score_explanation: str = ""


class BaseTextClassification(ABC):
    @abstractmethod
    def score_text(self, text: str) -> Score:
        """Score the text and return a Score object."""
        raise NotImplementedError("score_text method not implemented")
