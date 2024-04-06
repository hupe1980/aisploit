from typing import Sequence


class BaseCallbackHandler:
    def on_redteam_attempt_start(self, attempt: int, prompt: str):
        pass

    def on_redteam_attempt_end(self, attempt: int, response: str):
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

    def on_redteam_attempt_start(self, attempt: int, prompt: str):
        for cb in self._callbacks:
            cb.on_redteam_attempt_start(attempt, prompt)

    def on_redteam_attempt_end(self, attempt: int, response: str):
        for cb in self._callbacks:
            cb.on_redteam_attempt_end(attempt, response)
