from abc import ABC, abstractmethod

from .prompt import BasePromptValue


class BaseTarget(ABC):
    @abstractmethod
    def send_prompt(self, prompt: BasePromptValue) -> str:
        pass
