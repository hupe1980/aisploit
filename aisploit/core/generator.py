from abc import ABC, abstractmethod
from typing import Any, Generator, Generic, TypeVar

T = TypeVar("T")


class BaseGenerator(Generic[T], ABC):
    @abstractmethod
    def generate(self) -> Generator[T, Any, None]:
        pass
