from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from .model import BaseChatModel
from .prompt import BasePromptValue, StringPromptValue


class BaseConverter(ABC):
    """Abstract base class for converters."""

    @abstractmethod
    def _convert(self, prompt: str) -> str:
        """Converts the prompt string.

        Args:
            prompt (str): The prompt string to be converted.

        Returns:
            str: The converted prompt string.
        """
        pass

    def convert(self, prompt: Union[str, BasePromptValue]) -> BasePromptValue:
        """Converts the prompt value.

        Args:
            prompt (BasePromptValue): The prompt value to be converted.

        Returns:
            BasePromptValue: The converted prompt value.
        """
        if isinstance(prompt, str):
            return StringPromptValue(text=self._convert(prompt))

        if isinstance(prompt, StringPromptValue):
            return StringPromptValue(text=self._convert(prompt.text))

        return prompt

    def __repr__(self) -> str:
        """Return a string representation of the converter.

        Returns:
            str: A string representation of the converter.
        """
        prefix = "aisploit"
        if not self.__module__.startswith(prefix):
            prefix = "custom"

        return f"<{prefix}.{self.__class__.__name__}>"


@dataclass
class BaseChatModelConverter(BaseConverter, ABC):
    chat_model: BaseChatModel

    def __repr__(self) -> str:
        """Return a string representation of the converter.

        Returns:
            str: A string representation of the converter.
        """
        prefix = "aisploit"
        if not self.__module__.startswith(prefix):
            prefix = "custom"

        return f"<{prefix}.{self.__class__.__name__}(chat_model={self.chat_model.get_name()})>"
