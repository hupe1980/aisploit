from typing import Callable


from ..core import BaseTarget


class WrapperTarget(BaseTarget):
    def __init__(self, func: Callable) -> None:
        self._func = func

    def send_prompt(self, prompt: str) -> str:
        return self._func(prompt)


def target(func: Callable) -> WrapperTarget:
    return WrapperTarget(func)
