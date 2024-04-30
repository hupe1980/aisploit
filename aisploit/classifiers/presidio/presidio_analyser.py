from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult

from ...core import BaseTextClassifier, Score


@dataclass(kw_only=True)
class PresidioAnalyserClassifier(BaseTextClassifier[List[RecognizerResult]]):
    """A text classifier using the Presidio Analyzer for detecting Personally Identifiable Information (PII)."""

    language: str = "en"
    entities: List[str] | None = None
    threshold: float = 0.7
    additional_recognizers: List[EntityRecognizer] = field(default_factory=list)
    filter_func: Optional[Callable[[str, RecognizerResult], bool]] = None
    tags: List[str] = field(default_factory=lambda: ["leakage"], init=False)

    def __post_init__(self) -> None:
        """Initialize the Presidio Analyzer engine."""
        # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
        self._analyzer = AnalyzerEngine(default_score_threshold=self.threshold)

        for recognizer in self.additional_recognizers:
            self._analyzer.registry.add_recognizer(recognizer=recognizer)

    def score(
        self, input: str, references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[List[RecognizerResult]]:
        """Score the input text for Personally Identifiable Information (PII) entities.

        Args:
            input (str): The input text to be scored.
            _references: List[str], optional): Ignored parameter. Defaults to None.

        Returns:
            Score[List[RecognizerResult]]: A Score object representing the results of PII detection.
        """
        results = self._analyzer.analyze(text=input, entities=self.entities, language=self.language)

        if self.filter_func:
            results = [result for result in results if self.filter_func(input, result)]

        return Score[List[RecognizerResult]](
            flagged=len(results) > 0,
            value=results,
            description="Returns True if entities are found in the input",
            explanation=(
                f"Found {len(results)} entities in input" if len(results) > 0 else "Did not find entities in input"
            ),
        )
