from ..core import BaseConverter


class LowercaseConverter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        return prompt.lower()


class UppercaseConverter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        return prompt.upper()


class TitlecaseConverter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        return prompt.title()
