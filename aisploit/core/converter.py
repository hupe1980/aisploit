from abc import ABC, abstractmethod

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, prompts: list[str]) -> list[str]:
            pass