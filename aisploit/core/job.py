from dataclasses import dataclass
from uuid import uuid4


@dataclass(kw_only=True)
class BaseJob:
    verbose: bool = False

    def _create_run_id(self) -> str:
        return str(uuid4())
