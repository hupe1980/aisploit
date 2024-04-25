from dataclasses import dataclass, field
from typing import Any, Dict, List

import evaluate

from ...core import BaseTextClassifier, Score


@dataclass
class BleuClassifier(BaseTextClassifier[Dict[str, Any]]):
    """A classifier that computes BLEU score for text inputs."""

    threshold: float = 0.2
    bleu: evaluate.EvaluationModule = field(default_factory=lambda: evaluate.load("bleu"), init=False)

    def score(
        self, input: str, references: List[str] | None = None, _metadata: Dict[str, Any] | None = None
    ) -> Score[Dict[str, Any]]:
        """Score the input using BLEU score computed by the evaluate module.

        Args:
            input (str): The input text to be scored.
            references (List[str], optional): List of reference texts. Defaults to None.

        Raises:
            ValueError: If the number of references is not equal to 1.

        Returns:
            Score[Dict[str, Any]]: A Score object representing the BLEU score of the input.
        """
        if not references or not len(references) == 1:
            raise ValueError("The number of references must be exactly 1.")

        score = self.bleu.compute(
            predictions=[input],
            references=[references[0]],
            max_order=2,
        )

        bleu_score = score["bleu"]

        return Score[Dict[str, Any]](
            flagged=bleu_score < self.threshold,
            value=score,
            description="Returns True if the bleu score is less than the threshold",
            explanation=f"The bleu score for the input and reference is {bleu_score}",
        )
