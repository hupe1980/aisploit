import sys
from dataclasses import dataclass, field
from typing import IO

from ..core import BasePromptValue, BaseTarget, Response


@dataclass
class StdOutTarget(BaseTarget):
    text_stream: IO[str] = field(default=sys.stdout)

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        self.text_stream.write(f"{prompt.to_string()}\n")
        return Response(content=f"Prompt printed to stream {self.text_stream.name}.")
