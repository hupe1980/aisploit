from ..core import BaseConverter


class NoOpConverter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        return prompt
