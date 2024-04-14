from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)

from ...core import BaseTextClassifier, Score


class PipelinePromptInjectionIdentifier(BaseTextClassifier[float]):
    def __init__(
        self,
        *,
        model_name: str = "laiyer/deberta-v3-base-prompt-injection",
        injection_label: str = "INJECTION",
        threshold: float = 0.5,
    ) -> None:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        self._model = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            max_length=512,  # default length of BERT models
            truncation=True,  # otherwise it will fail on long prompts
        )

        self._injection_label = injection_label
        self._threshold = threshold

    def score(self, input: str) -> Score[float]:
        result = self._model(input)

        score = result[0]["score"] if result[0]["label"] == self._injection_label else 1 - result[0]["score"]

        explanation = "Prompt injection attack detected" if score > self._threshold else "No prompt injection"

        return Score[float](
            flagged=score > self._threshold,
            value=score,
            description="Prompt injection detection score",
            explanation=explanation,
        )
