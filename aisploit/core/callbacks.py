from typing import Sequence

from .prompt import BasePromptValue
from .classifier import Score


class BaseCallbackHandler:
    def on_redteam_attempt_start(
        self, attempt: int, prompt: BasePromptValue, *, run_id: str
    ):
        pass

    def on_redteam_attempt_end(
        self, attempt: int, response: str, score: Score, *, run_id: str
    ):
        pass

    def on_scanner_plugin_start(self, name: str, *, run_id: str):
        pass

    def on_scanner_plugin_end(self, name: str, *, run_id: str):
        pass


Callbacks = Sequence[BaseCallbackHandler]


class CallbackManager:
    def __init__(
        self,
        *,
        run_id: str,
        callbacks: Sequence[BaseCallbackHandler] = [],
    ) -> None:
        self.run_id = run_id
        self._callbacks = callbacks

    def on_redteam_attempt_start(self, attempt: int, prompt: BasePromptValue):
        for cb in self._callbacks:
            cb.on_redteam_attempt_start(
                attempt=attempt, prompt=prompt, run_id=self.run_id
            )

    def on_redteam_attempt_end(self, attempt: int, response: str, score: Score):
        for cb in self._callbacks:
            cb.on_redteam_attempt_end(
                attempt=attempt, response=response, score=score, run_id=self.run_id
            )

    def on_scanner_plugin_start(self, name: str):
        for cb in self._callbacks:
            cb.on_scanner_plugin_start(name=name, run_id=self.run_id)

    def on_scanner_plugin_end(self, name: str):
        for cb in self._callbacks:
            cb.on_scanner_plugin_end(name=name, run_id=self.run_id)
