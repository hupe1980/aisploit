from typing import Sequence

from .classifier import Score
from .prompt import BasePromptValue
from .target import Response


class BaseCallbackHandler:
    """Base class for callback handlers."""

    def on_redteam_attempt_start(self, attempt: int, prompt: BasePromptValue, *, run_id: str):
        """Called when a red team attempt starts.

        Args:
            attempt (int): The attempt number.
            prompt (BasePromptValue): The prompt value.
            run_id (str): The ID of the current run.
        """
        pass

    def on_redteam_attempt_end(self, attempt: int, response: Response, score: Score, *, run_id: str):
        """Called when a red team attempt ends.

        Args:
            attempt (int): The attempt number.
            response (Response): The response from the attempt.
            score (Score): The score of the attempt.
            run_id (str): The ID of the current run.
        """
        pass

    def on_scanner_plugin_start(self, name: str, *, run_id: str):
        """Called when a scanner plugin starts.

        Args:
            name (str): The name of the scanner plugin.
            run_id (str): The ID of the current run.
        """
        pass

    def on_scanner_plugin_end(self, name: str, *, run_id: str):
        """Called when a scanner plugin ends.

        Args:
            name (str): The name of the scanner plugin.
            run_id (str): The ID of the current run.
        """
        pass

    def on_sender_send_prompt_start(self):
        pass

    def on_sender_send_prompt_end(self):
        pass


Callbacks = Sequence[BaseCallbackHandler]


class CallbackManager:
    """Manages callback handlers."""

    def __init__(
        self,
        *,
        run_id: str,
        callbacks: Sequence[BaseCallbackHandler] | None,
    ) -> None:
        """Initialize the CallbackManager.

        Args:
            run_id (str): The ID of the current run.
            callbacks (Sequence[BaseCallbackHandler], optional): The list of callback handlers. Defaults to [].
        """
        self.run_id = run_id
        self._callbacks = callbacks or []

    def on_redteam_attempt_start(self, attempt: int, prompt: BasePromptValue):
        """Notify callback handlers when a red team attempt starts.

        Args:
            attempt (int): The attempt number.
            prompt (BasePromptValue): The prompt value.
        """
        for cb in self._callbacks:
            cb.on_redteam_attempt_start(attempt=attempt, prompt=prompt, run_id=self.run_id)

    def on_redteam_attempt_end(self, attempt: int, response: Response, score: Score):
        """Notify callback handlers when a red team attempt ends.

        Args:
            attempt (int): The attempt number.
            response (Response): The response from the attempt.
            score (Score): The score of the attempt.
        """
        for cb in self._callbacks:
            cb.on_redteam_attempt_end(attempt=attempt, response=response, score=score, run_id=self.run_id)

    def on_scanner_plugin_start(self, name: str):
        """Notify callback handlers when a scanner plugin starts.

        Args:
            name (str): The name of the scanner plugin.
        """
        for cb in self._callbacks:
            cb.on_scanner_plugin_start(name=name, run_id=self.run_id)

    def on_scanner_plugin_end(self, name: str):
        """Notify callback handlers when a scanner plugin ends.

        Args:
            name (str): The name of the scanner plugin.
        """
        for cb in self._callbacks:
            cb.on_scanner_plugin_end(name=name, run_id=self.run_id)

    def on_sender_send_prompt_start(self):
        for cb in self._callbacks:
            cb.on_sender_send_prompt_start()

    def on_sender_send_prompt_end(self):
        for cb in self._callbacks:
            cb.on_sender_send_prompt_end()
