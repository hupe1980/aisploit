from dataclasses import dataclass
from typing import Callable

from ..core import BasePromptValue, BaseTarget, Response


@dataclass
class WrapperTarget(BaseTarget):
    func: Callable

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        content = self.func(prompt)
        return Response(content=content)


def target(func: Callable) -> WrapperTarget:
    return WrapperTarget(func)
