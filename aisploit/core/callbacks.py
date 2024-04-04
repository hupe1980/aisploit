from typing import List


class BaseCallbackHandler:
    def on_redteam_attempt(self, attempt: int, prompt: str):
        pass

    def on_redteam_attempt_response(self, attempt: int, response: str):
        pass

Callbacks = List[BaseCallbackHandler]

class CallbackManager:
    def __init__(
        self, 
        *,
        id: str,
        callbacks: List[BaseCallbackHandler] = [],
    ) -> None:
        self.id = id
        self._callbacks = callbacks

    def on_redteam_attempt(self, attempt: int, prompt: str):
        for cb in self._callbacks:
            cb.on_redteam_attempt(attempt, prompt)

    def on_redteam_attempt_response(self, attempt: int, response: str):
        for cb in self._callbacks:
            cb.on_redteam_attempt_response(attempt, response)