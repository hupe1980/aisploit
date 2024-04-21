from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, TypeVar

import boto3

from ...core import BaseTextClassifier, Score

T = TypeVar("T")


@dataclass
class BaseComprehendClassifier(BaseTextClassifier[T], Generic[T]):
    session: boto3.Session = field(default_factory=lambda: boto3.Session())
    region_name: str = "us-east-1"

    def __post_init__(self):
        self._client = self.session.client("comprehend", region_name=self.region_name)


@dataclass
class ComprehendPIIClassifier(BaseComprehendClassifier[List[Any]]):
    language: str = "en"
    threshold: float = 0.7

    def score(self, input: str) -> Score[List[Any]]:
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
    language: str = "en"
    threshold: float = 0.7

    def score(self, input: str) -> Score[Dict[str, Any]]:
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
