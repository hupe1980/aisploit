from abc import ABC, abstractmethod
from langchain_core.prompt_values import StringPromptValue
from .prompt import BasePromptValue


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

    def convert(self, prompt: BasePromptValue) -> BasePromptValue:
        """Converts the prompt value.

        Args:
            prompt (BasePromptValue): The prompt value to be converted.

        Returns:
            BasePromptValue: The converted prompt value.
        """
        if isinstance(prompt, StringPromptValue):
            prompt = StringPromptValue(text=self._convert(prompt.text))

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
