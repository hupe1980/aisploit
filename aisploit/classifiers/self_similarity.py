from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from ..core import BaseTextClassifier, Score


@dataclass
class SelfSimilarityClassifier(BaseTextClassifier[Dict[str, Any]]):
    """A text classifier based on self-similarity using cosine similarity scores."""

    model_name_or_path: str = "all-MiniLM-L6-v2"
    threshold: float = 0.7
    aggregation: Literal["mean", "min"] = "mean"
    tags: List[str] = field(default_factory=lambda: ["hallucination"], init=False)

    def __post_init__(self) -> None:
        """Initialize the SentenceTransformer model."""
        self._model = SentenceTransformer(self.model_name_or_path)

    def score(self, input: str, references: List[str] | None = None) -> Score[Dict[str, Any]]:
        """Score the input text based on its self-similarity to reference texts.

        Args:
            input (str): The input text to be scored.
            references (List[str], optional): List of reference texts. Defaults to None.

        Raises:
            ValueError: If references is None or if the number of references is not at least 1.

        Returns:
            Score[Dict[Any]]: A Score object representing the self-similarity score of the input.
        """
        if not references or not len(references) >= 1:
            raise ValueError("The number of references must be at least 1.")

        input_embeddings = self._model.encode(input, convert_to_tensor=True)
        references_embeddings = self._model.encode(references, convert_to_tensor=True)

        cos_scores = cos_sim(input_embeddings, references_embeddings)[0]

        score = cos_scores.mean() if self.aggregation == "mean" else cos_scores.min()

        return Score[Dict[str, Any]](
            flagged=(score < self.threshold).item(),
            value={
                "aggregated_score": score.item(),
                "scores": cos_scores.tolist(),
            },
            description="Returns True if the aggregated cosine similarity score is less than the threshold",
            explanation=f"The aggregated cosine similarity score for the input is {score}",
        )
