import base64
from dataclasses import dataclass

from ..core import BaseConverter


@dataclass
class Base64Converter(BaseConverter):
    prefix: str = "The following instruction is base64 encoded:"
    add_prefix: bool = True

    def _convert(self, prompt: str) -> str:
        b64_string = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
        if self.add_prefix and not b64_string == "":
            return f"{self.prefix} {b64_string}"
        else:
            return b64_string
