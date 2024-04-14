import sys
from typing import IO

from ..core import BasePromptValue, BaseTarget, Response


class StdOutTarget(BaseTarget):
    def __init__(
        self,
        *,
        text_stream: IO[str] = sys.stdout,
    ) -> None:
        self._text_stream = text_stream

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        self._text_stream.write(f"{prompt.to_string()}\n")
        return Response(content=f"Prompt printed to stream {self._text_stream.name}.")
