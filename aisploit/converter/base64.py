import base64

from ..core import BaseConverter


class Base64Converter(BaseConverter):
    def convert(self, prompts: list[str]) -> list[str]:
        return [
            base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
            for prompt in prompts
        ]
