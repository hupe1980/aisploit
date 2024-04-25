from dataclasses import dataclass
from typing import Any, Dict, List

from ..core import BaseTextClassifier, Score


@dataclass
class RepeatedTokenClassifier(BaseTextClassifier[bool]):
    def score(
        self, input: str, _references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[bool]:
        if not metadata:
            raise ValueError("metadata  is missing")

        repeated_token = metadata.get("repeated_token")

        if not repeated_token:
            raise ValueError("metadata with repeated token is missing")

        # TODO

        return Score[bool](
            flagged=False,
            value=False,
            description="TODO",
            explanation="TODO",
        )
