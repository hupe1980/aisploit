from typing import Dict, Optional

from langchain_core.utils.utils import convert_to_secret_str
from langchain_google_genai import (
    ChatGoogleGenerativeAI as LangchainChatGoogleGenerativeAI,
)
from langchain_google_genai import (
    HarmBlockThreshold,
    HarmCategory,
)

from ..core import BaseChatModel

block_none_harm_category = {
    HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
}


class ChatGoogleGenerativeAI(LangchainChatGoogleGenerativeAI, BaseChatModel):
    """
    Wrapper class for interacting with the Google Generative AI API for chat-based models.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "gemini-pro",
        max_output_tokens: int = 1024,
        temperature: float = 1.0,
        safety_settings: Dict[HarmCategory, HarmBlockThreshold] | None = None,
        **kwargs
    ) -> None:
        """
        Initialize the ChatGoogleGenerativeAI instance.

        Args:
            api_key (Optional[str]): The API key for accessing the Google Generative AI API.
            model (str): The name of the model to use (default is "gemini-pro").
            max_output_tokens (int): The maximum number of tokens to generate in the response.
            temperature (float): The temperature parameter for controlling randomness in the generated text.
            safety_settings (dict): Safety settings to control blocking thresholds for various harm categories.
            **kwargs: Additional keyword arguments passed to the base class initializer.
        """
        super().__init__(
            google_api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            safety_settings=safety_settings if safety_settings else block_none_harm_category, # type: ignore
            **kwargs,
        )

    def supports_functions(self) -> bool:
        """
        Check if the model supports additional functions beyond basic chat.

        Returns:
            bool: True if the model supports additional functions, False otherwise.
        """
        return False
