from typing import Optional
from langchain_core.utils.utils import convert_to_secret_str
from langchain_openai import ChatOpenAI as LangchainChatOpenAI

from ..core import BaseChatModel


class ChatOpenAI(LangchainChatOpenAI, BaseChatModel):
    """
    Wrapper class for interacting with the OpenAI API for chat-based models.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str],
        model: str = "gpt-4",
        max_tokens: int = 1024,
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        """
        Initialize the ChatOpenAI instance.

        Parameters:
        - api_key (Optional[str]): The API key for accessing the OpenAI API.
        - model (str): The name of the model to use (e.g., "gpt-4").
        - max_tokens (int): The maximum number of tokens to generate in the response.
        - temperature (float): The temperature parameter for generating diverse responses.
        - **kwargs: Additional keyword arguments passed to the base class initializer.
        """
        super().__init__(
            api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

    def supports_functions(self) -> bool:
        return True
