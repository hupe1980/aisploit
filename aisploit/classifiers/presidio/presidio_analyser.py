from dataclasses import dataclass, field
from typing import List

from presidio_analyzer import AnalyzerEngine, RecognizerResult

from ...core import BaseTextClassifier, Score


@dataclass
class PresidioAnalyserClassifier(BaseTextClassifier[List[RecognizerResult]]):

    language: str = "en"
    entities: List[str] | None = None
    threshold: float = 0.7
    tags: List[str] = field(default_factory=lambda: ["leakage"], init=False)

    def __post_init__(self) -> None:
        # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
        self._analyzer = AnalyzerEngine(default_score_threshold=self.threshold)

    def score(self, input: str, references: List[str] | None = None) -> Score[List[RecognizerResult]]:
        # Call analyzer to get results
        results = self._analyzer.analyze(text=input, entities=self.entities, language=self.language)

        return Score[List[RecognizerResult]](
            flagged=len(results) > 0,
            value=results,
            description="Returns True if entities are found in the input",
            explanation=(
                f"Found {len(results)} entities in input" if len(results) > 0 else "Did not find entities in input"
            ),
        )
