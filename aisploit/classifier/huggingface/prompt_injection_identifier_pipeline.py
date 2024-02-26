from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)
from aisploit.core import BaseTextClassification, Score


class PromptIjectionIdentifierPipeline(BaseTextClassification):
    def __init__(
        self,
        *,
        model_name: str = "laiyer/deberta-v3-base-prompt-injection",
        injection_label: str = "INJECTION",
        threshold: float = 0.5,
    ) -> None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
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

    def score_text(self, text: str) -> Score:
        result = self._model(text)

        score = (
            result[0]["score"]
            if result[0]["label"] == self._injection_label
            else 1 - result[0]["score"]
        )

        explanation = (
            "Prompt injection attack detected"
            if score > self._threshold
            else "No prompt injection"
        )

        return Score(
            score_type="float",
            score_value=score,
            score_description="Prompt injection detection score",
            score_explanation=explanation,
        )
