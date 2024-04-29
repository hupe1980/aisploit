from dataclasses import dataclass

from ..core import BaseConverter


@dataclass
class UnicodeTagsConverter(BaseConverter):
    prefix: str = ""
    suffix: str = ""
    add_sequence_markers: bool = False

    def _convert(self, prompt: str) -> str:
        encoded = ""

        if self.add_sequence_markers:
            encoded += chr(0xE0001)

        encoded = ''.join(chr(0xE0000 + ord(ch)) for ch in prompt)

        if self.add_sequence_markers:
            encoded += chr(0xE007F)

        return self.prefix + encoded + self.suffix
