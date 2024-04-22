import os
from typing import List, Optional

from openai import OpenAI
from openai.types.moderation import Moderation

from ...core import BaseTextClassifier, Score


class ModerationClassifier(BaseTextClassifier[Moderation]):
    """A classifier that uses the OpenAI Moderations API for scoring."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
    ) -> None:
        if not api_key:
            api_key = os.environ["OPENAI_API_KEY"]

        self._client = OpenAI(api_key=api_key)

    def score(self, input: str, _: List[str] | None = None) -> Score[Moderation]:
        """Score the input using the OpenAI Moderations API.

        Args:
            input (str): The input text to be scored.
            _: List of references (ignored).

        Returns:
            Score[Moderation]: A Score object representing the moderation score of the input.
        """
        response = self._client.moderations.create(input=input)
        output = response.results[0]

        return Score[Moderation](
            flagged=output.flagged,
            value=output,
            description="Moderation score for the given input",
            explanation="Details about the moderation score",
        )
