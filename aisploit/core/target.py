from abc import ABC, abstractmethod


class BaseTarget(ABC):
    @abstractmethod
    def send_prompt(self, prompt: str) -> str:
        pass
