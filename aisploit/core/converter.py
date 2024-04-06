from abc import ABC, abstractmethod
from langchain_core.prompt_values import StringPromptValue
from .prompt import BasePromptValue


class BaseConverter(ABC):
    @abstractmethod
    def _convert(self, prompt: str) -> str:
        pass

    def convert(self, prompt: BasePromptValue) -> BasePromptValue:
        if isinstance(prompt, StringPromptValue):
            prompt = StringPromptValue(text=self._convert(prompt.text))

        return prompt

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}()>"
