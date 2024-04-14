from typing import Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .prompt import BasePromptValue


@dataclass
class Response:
    """A class representing a response from the target."""

    content: str

    metadata: Dict[str, Any] = field(default_factory=dict)

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
