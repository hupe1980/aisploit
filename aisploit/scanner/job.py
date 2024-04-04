from typing import Optional, List
from uuid import uuid4


from ..core import BaseJob, BaseTarget, BaseCallbackHandler, CallbackManager
from ..dataset import Dataset


class ScannerJob(BaseJob):
    def __init__(
        self,
        *,
        target: BaseTarget,
        dataset: Optional[Dataset] = None,
        callbacks: List[BaseCallbackHandler] = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)
        self.scan_id = str(uuid4())
        self._target = target

        self._callback_manager = CallbackManager(
            id=self.scan_id,
            callbacks=callbacks,
        )

    def execute(self):
        for prompt in ["todo", "test", "foo", "bar"]:
            self._target.send_prompt(prompt)
