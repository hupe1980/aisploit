from typing import Optional

from langchain_anthropic import ChatAnthropic as LangchainChatAnthropic
from langchain_core.utils.utils import convert_to_secret_str

from ..core import BaseChatModel


class ChatAnthropic(LangchainChatAnthropic, BaseChatModel):
    """A chat model based on Anthropic's language generation technology."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model_name: str = "claude-3-opus-20240229",
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        """
        Initialize the ChatAnthropic instance.

        Args:
            api_key (str or None): The API key for accessing the Anthropic API.
            model_name (str): The name of the language model to use.
            temperature (float): The temperature parameter controlling the randomness of the generated text.
            **kwargs: Additional keyword arguments to be passed to the base class constructor.
        """
        super().__init__(
            api_key=convert_to_secret_str(api_key) if api_key else None,
            model_name=model_name,
            temperature=temperature,
            **kwargs,
        )

    def supports_functions(self) -> bool:
        """
        Check if the model supports additional functions beyond basic chat.

        Returns:
            bool: True if the model supports additional functions, False otherwise.
        """
        return False
