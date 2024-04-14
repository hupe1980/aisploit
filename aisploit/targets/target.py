from typing import Callable


from ..core import BaseTarget, Response, BasePromptValue


class WrapperTarget(BaseTarget):
    def __init__(self, func: Callable) -> None:
        self._func = func

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        content = self._func(prompt)
        return Response(content=content)


def target(func: Callable) -> WrapperTarget:
    return WrapperTarget(func)
