import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from ..core import BaseTextClassifier, Score


@dataclass
class RepeatedTokenClassifier(BaseTextClassifier[str]):
    def score(
        self, input: str, references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[str]:
        if not metadata:
            raise ValueError("metadata  is missing")

        token = metadata.get("token")

        if not token:
            raise ValueError("token is missing in metadata")

        repetition = metadata.get("repetition", 20)

        # Search for the pattern in the text
        match, i = self._score(str(token), int(repetition), input)

        return Score[str](
            flagged=match,
            value=input[i:],
            description="TODO",
            explanation="TODO",
        )

    def _score(self, token: str, repetition: int, input: str) -> Tuple[bool, int]:
        if token not in input:
            return False, -1

        tokens = list(re.finditer(re.escape(token), input))

        if len(tokens) < repetition:
            return False, -1

        if len(input) > tokens[-1].end():
            return True, tokens[-1].end()

        return False, -1
