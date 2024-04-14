import string
from ..core import BaseConverter


class RemovePunctuationConverter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        translator = str.maketrans("", "", string.punctuation)
        return prompt.translate(translator)
