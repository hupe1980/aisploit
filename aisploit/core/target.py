import base64
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Literal

from PIL import Image

from .prompt import BasePromptValue


class ContentFilteredException(Exception):
    pass


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


@dataclass
class BaseImageTarget(ABC):
    size: Literal["512x512", "1024x1024"] = "512x512"
    show_image: bool = False

    def _show_base64_image(self, base64_image: str) -> None:
        base64_bytes = base64_image.encode("ascii")
        image_bytes = base64.b64decode(base64_bytes)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()
