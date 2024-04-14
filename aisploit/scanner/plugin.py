from abc import ABC, abstractmethod
from typing import Sequence

from .report import Issue
from ..core import BaseTarget


class Plugin(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        pass
