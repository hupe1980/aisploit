from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .dataset import BaseDataset

T = TypeVar("T")


class BaseGenerator(Generic[T], ABC):
    @abstractmethod
    def generate_dataset(self) -> BaseDataset[T]:
        pass
