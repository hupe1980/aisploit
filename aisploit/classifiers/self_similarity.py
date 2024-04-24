from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

import torch
import torch.utils

from ..core import BaseEmbeddings, BaseTextClassifier, Score
from ..embeddings import HuggingFaceEmbeddings


@dataclass(kw_only=True)
class SelfSimilarityClassifier(BaseTextClassifier[Dict[str, Any]]):
    """A text classifier based on self-similarity using cosine similarity scores."""

    embeddings: BaseEmbeddings = field(default_factory=lambda: HuggingFaceEmbeddings())
    threshold: float = 0.7
    aggregation: Literal["mean", "min"] = "mean"
    tags: List[str] = field(default_factory=lambda: ["hallucination"], init=False)

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

        input_embeddings = torch.tensor(self.embeddings.embed_query(input))

        references_embeddings = torch.tensor(self.embeddings.embed_documents(references))

        # Calculate cosine similarity
        cos_scores = torch.nn.functional.cosine_similarity(input_embeddings.unsqueeze(0), references_embeddings, dim=1)

        score = cos_scores.mean() if self.aggregation == "mean" else cos_scores.min()

        return Score[Dict[str, Any]](
            flagged=bool(score < self.threshold),
            value={
                "aggregated_score": score.item(),
                "scores": cos_scores.tolist(),
            },
            description="Returns True if the aggregated cosine similarity score is less than the threshold",
            explanation=f"The aggregated cosine similarity score for the input is {score}",
        )
