from abc import ABC, abstractmethod
from .dataset import BaseDataset


class BaseGenerator(ABC):
    @abstractmethod
    def generate_dataset(self) -> BaseDataset:
        pass
