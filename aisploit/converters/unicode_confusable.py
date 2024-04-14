import random

from confusables import confusable_characters

from ..core import BaseConverter


class UnicodeConfusableConverter(BaseConverter):
    def __init__(self, *, random_state=None) -> None:
        if random_state is not None:
            random.seed(random_state)

    def _convert(self, prompt: str) -> str:
        return "".join(self._replace_with_confusable(c) for c in prompt)

    def _replace_with_confusable(self, char: str) -> str:
        confusable_options = confusable_characters(char)
        if not confusable_options or char == " ":
            return char

        return random.choice(confusable_options)
