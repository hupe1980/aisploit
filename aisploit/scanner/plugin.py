from typing import Dict, Optional, Sequence
from abc import ABC, abstractmethod
from collections import defaultdict


from ..core import BaseTarget
from .issue import Issue


class Plugin(ABC):
    @abstractmethod
    def run(self, target: BaseTarget) -> Sequence[Issue]:
        pass


class PluginRegistry:
    _detectors: Dict[str, type[Plugin]] = dict()
    _tags = defaultdict[str, set](set)

    @classmethod
    def register(
        cls, name: str, detector: type[Plugin], tags: Optional[Sequence[str]] = None
    ):
        cls._detectors[name] = detector
        if tags is not None:
            cls._tags[name] = set(tags)

    @classmethod
    def get_plugin_classes(cls, tags: Optional[Sequence[str]] = None) -> dict:
        if tags is None:
            return {n: d for n, d in cls._detectors.items()}

        return {
            n: d for n, d in cls._detectors.items() if cls._tags[n].intersection(tags)
        }
