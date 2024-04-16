from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from .report import Issue
from ..core import BaseTarget


@dataclass
class Plugin(ABC):
    name: str

    @abstractmethod
    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        pass
