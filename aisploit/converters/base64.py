import base64

from ..core import BaseConverter


class Base64Converter(BaseConverter):
    def _convert(self, prompt: str) -> str:
        return base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
