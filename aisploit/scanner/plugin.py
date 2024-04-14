from typing import Sequence
from abc import ABC, abstractmethod


from ..core import BaseTarget
from .report import Issue


class Plugin(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        pass
