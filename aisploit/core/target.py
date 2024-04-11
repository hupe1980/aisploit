from abc import ABC, abstractmethod
from dataclasses import dataclass

from .prompt import BasePromptValue


@dataclass(frozen=True)
class Response:
    """A class representing a response from a target.

    Attributes:
        content (str): The content of the response.
    """

    content: str

    def __repr__(self) -> str:
        """Return a string representation of the Response."""
        return f"content={repr(self.content)}"


class BaseTarget(ABC):
    """An abstract base class for targets."""

    @abstractmethod
    def send_prompt(self, prompt: BasePromptValue) -> Response:
        """Send a prompt to the target and return the response.

        Args:
            prompt (BasePromptValue): The prompt to send.

        Returns:
            Response: The response from the target.
        """
        pass
