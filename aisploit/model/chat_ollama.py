from langchain_community.chat_models import ChatOllama as LangchainChatOllama

from ..core import BaseChatModel


class ChatOllama(LangchainChatOllama, BaseChatModel):
    """
    Wrapper class for interacting with the ChatOllama model.
    """

    def __init__(
        self,
        *,
        model: str = "llama2",
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        """
        Initialize the ChatOllama instance.

        Parameters:
        - model (str): The name of the model to use (default is "llama2").
        - temperature (float): The temperature parameter for generating diverse responses.
        - **kwargs: Additional keyword arguments passed to the base class initializer.
        """
        super().__init__(
            model=model,
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
