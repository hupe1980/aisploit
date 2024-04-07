import re
from ..core import BaseClassifier, Score


class RegexClassifier(BaseClassifier[bool]):
    def __init__(self, *, pattern: re.Pattern, flag_matches=True) -> None:
        self._pattern = pattern
        self._flag_matches = flag_matches

    def score_text(self, text: str) -> Score[bool]:
        if re.search(self._pattern, text):
            return Score[bool](
                flagged=True if self._flag_matches else False,
                value=True,
                description=f"Return True if the pattern {self._pattern.pattern} is found in the text",
                explanation=f"Found pattern {self._pattern.pattern} in text",
            )

        return Score[bool](
            flagged=False if self._flag_matches else True,
            value=False,
            description=f"Return True if the pattern {self._pattern.pattern} is found in the text",
            explanation=f"Did not find pattern {self._pattern.pattern} in text",
        )


class SubstringClassifier(RegexClassifier):
    def __init__(self, *, substring: str, ignore_case=True, flag_matches=True) -> None:
        compiled_pattern = (
            re.compile(substring, re.IGNORECASE)
            if ignore_case
            else re.compile(substring)
        )
        super().__init__(pattern=compiled_pattern, flag_matches=flag_matches)
