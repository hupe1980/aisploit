import sys

from typing import IO


from ..core import BaseTarget


class StdOutTarget(BaseTarget):
    def __init__(self, text_stream: IO[str] = sys.stdout) -> None:
        self._text_stream = text_stream

    def send_prompt(self, prompt: str) -> str:
        self._text_stream.write(f"{prompt}\n")
        return prompt
