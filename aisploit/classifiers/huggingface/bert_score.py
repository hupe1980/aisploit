from dataclasses import dataclass, field
from typing import Any, Dict, List

import evaluate

from ...core import BaseTextClassifier, Score


@dataclass
class BertScoreClassifier(BaseTextClassifier[Dict[str, Any]]):
    """A classifier that computes BERTScore for text inputs."""

    threshold: float = 0.8
    model_type: str = "distilbert-base-uncased"
    bertscore: evaluate.EvaluationModule = field(default_factory=lambda: evaluate.load("bertscore"), init=False)

    def score(
        self, input: str, references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[Dict[str, Any]]:
        """Score the input using BERTScore computed by the evaluate module.

        Args:
            input (str): The input text to be scored.
            references (List[str], optional): List of reference texts. Defaults to None.

        Raises:
            ValueError: If references is None or if the number of references is not equal to 1.

        Returns:
            Score[Dict[str, Any]]: A Score object representing the BERTScore of the input.
        """
        if not references or not len(references) == 1:
            raise ValueError("The number of references must be exactly 1.")

        score = self.bertscore.compute(
            predictions=[input],
            references=[references[0]],
            model_type=self.model_type,
        )

        f1_score = score["f1"][0]

        return Score[Dict[str, Any]](
            flagged=f1_score < self.threshold,
            value=score,
            description="Returns True if the f1 score is less than the threshold",
            explanation=f"The f1 score for the input and reference is {f1_score}",
        )
