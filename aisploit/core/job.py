from abc import ABC
from uuid import uuid4


class BaseJob(ABC):
    def __init__(self, *, verbose=False) -> None:
        self.verbose = verbose

    def _create_run_id(self) -> str:
        return str(uuid4())
