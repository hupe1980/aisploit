from typing import Sequence

from langchain_core.prompt_values import StringPromptValue

from ..core import BaseConverter


class SequenceConverter(BaseConverter):
    def __init__(self, *, converters: Sequence[BaseConverter] = []) -> None:
        self._converters = converters

    def _convert(self, prompt: str) -> str:
        converted_prompt = prompt
        for converter in self._converters:
            converted_prompt = converter.convert(StringPromptValue(text=converted_prompt)).to_string()

        return converted_prompt
