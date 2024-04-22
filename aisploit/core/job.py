import sys
from dataclasses import dataclass, field
from uuid import uuid4

from ..utils import is_running_in_jupyter_notebook


@dataclass(kw_only=True)
class BaseJob:
    disable_progressbar: bool = field(
        default_factory=lambda: False if (is_running_in_jupyter_notebook() or sys.stdout.isatty()) else True
    )
    verbose: bool = False

    def _create_run_id(self) -> str:
        return str(uuid4())
