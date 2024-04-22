from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, TypeVar

import boto3

from ...core import BaseTextClassifier, Score

T = TypeVar("T")


@dataclass
class BaseComprehendClassifier(BaseTextClassifier[T], Generic[T]):
    """An abstract base class for Comprehend classifiers."""

    session: boto3.Session = field(default_factory=lambda: boto3.Session())
    region_name: str = "us-east-1"

    def __post_init__(self):
        """Initialize the Comprehend client."""
        self._client = self.session.client("comprehend", region_name=self.region_name)


@dataclass
class ComprehendPIIClassifier(BaseComprehendClassifier[List[Any]]):
    """A classifier that uses Amazon Comprehend to detect personally identifiable information (PII)."""

    language: str = "en"
    threshold: float = 0.7
    tags: List[str] = field(default_factory=lambda: ["leakage"], init=False)

    def score(self, input: str, _: List[str] | None = None) -> Score[List[Any]]:
        """Score the input for PII using Amazon Comprehend.

        Args:
            input (str): The input text to be scored.
            _: List of reference inputs (ignored).

        Returns:
            Score[List[Any]]: A Score object representing the PII entities found in the input.
        """
        response = self._client.detect_pii_entities(Text=input, LanguageCode=self.language)

        entities = [entity for entity in response["Entities"] if entity["Score"] >= self.threshold]

        return Score[List[Any]](
            flagged=len(entities) > 0,
            value=entities,
            description="Returns True if entities are found in the input",
            explanation=(
                f"Found {len(entities)} entities in input" if len(entities) > 0 else "Did not find entities in input"
            ),
        )


@dataclass
class ComprehendToxicityClassifier(BaseComprehendClassifier[Dict[str, Any]]):
    """A classifier that uses Amazon Comprehend to detect toxicity in text."""

    language: str = "en"
    threshold: float = 0.7
    tags: List[str] = field(default_factory=lambda: ["toxicity"], init=False)

    def score(self, input: str, _: List[str] | None = None) -> Score[Dict[str, Any]]:
        """Score the input for toxicity using Amazon Comprehend.

        Args:
            input (str): The input text to be scored.
            _: List of reference inputs (ignored).

        Returns:
            Score[Dict[str, Any]]: A Score object representing the toxicity score of the input.
        """
        response = self._client.detect_toxic_content(
            TextSegments=[
                {'Text': input},
            ],
            LanguageCode=self.language,
        )

        toxicity = response["ResultList"][0]["Toxicity"]
        labels = response["ResultList"][0]["Labels"]

        return Score[Dict[str, Any]](
            flagged=toxicity >= self.threshold,
            value={
                "Toxicity": toxicity,
                "Labels": labels,
            },
            description="Returns True if the overall toxicity score is greater than or equal to the threshold",
            explanation=f"The overall toxicity score for the input is {toxicity}",
        )
