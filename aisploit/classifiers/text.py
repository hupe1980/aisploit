import re
from dataclasses import dataclass
from typing import Any, Dict, List

from ..core import BaseTextClassifier, Score


class RegexClassifier(BaseTextClassifier[bool]):
    """A text classifier based on regular expressions."""

    def __init__(self, *, pattern: re.Pattern, flag_matches=True) -> None:
        """Initialize the RegexClassifier.

        Args:
            pattern (re.Pattern): The regular expression pattern to match.
            flag_matches (bool, optional): Flag indicating whether matches should be flagged. Defaults to True.
        """
        self._pattern = pattern
        self._flag_matches = flag_matches

    def score(
        self, input: str, references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[bool]:
        """Score the input based on the regular expression pattern.

        Args:
            input (str): The input text to be scored.

        Returns:
            Score[bool]: A Score object representing the result of scoring.
        """
        if re.search(self._pattern, input):
            return Score[bool](
                flagged=True if self._flag_matches else False,
                value=True,
                description=f"Return True if the pattern {self._pattern.pattern} is found in the input",
                explanation=f"Found pattern {self._pattern.pattern} in input",
            )

        return Score[bool](
            flagged=False if self._flag_matches else True,
            value=False,
            description=f"Return True if the pattern {self._pattern.pattern} is found in the input",
            explanation=f"Did not find pattern {self._pattern.pattern} in input",
        )


class SubstringClassifier(RegexClassifier):
    """A text classifier based on substring matching."""

    def __init__(self, *, substring: str, ignore_case=True, flag_matches=True) -> None:
        """Initialize the SubstringClassifier.

        Args:
            substring (str): The substring to match.
            ignore_case (bool, optional): Flag indicating whether to ignore case when matching substrings. Defaults to True.
            flag_matches (bool, optional): Flag indicating whether matches should be flagged. Defaults to True.
        """
        compiled_pattern = re.compile(substring, re.IGNORECASE) if ignore_case else re.compile(substring)
        super().__init__(pattern=compiled_pattern, flag_matches=flag_matches)


@dataclass
class TextTokenClassifier(BaseTextClassifier[bool]):
    token: str

    def score(
        self, input: str, references: List[str] | None = None, metadata: Dict[str, Any] | None = None
    ) -> Score[bool]:
        return Score[bool](
            flagged=self.token in input,
            value=self.token in input,
            description=f"Return True if the token {self.token} is found in the input",
            explanation=(
                f"Found token {self.token} in input"
                if self.token in input
                else f"Did not find token {self.token} in input"
            ),
        )
