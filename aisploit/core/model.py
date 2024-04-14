from abc import abstractmethod
from typing import Union

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable


class BaseLLM(Runnable[LanguageModelInput, str]):
    pass


class BaseChatModel(Runnable[LanguageModelInput, BaseMessage]):
    @abstractmethod
    def supports_functions(self) -> bool:
        """
        Check if the model supports additional functions beyond basic chat.

        Returns:
            bool: True if the model supports additional functions, False otherwise.
        """
        pass


BaseModel = Union[BaseLLM, BaseChatModel]

BaseEmbeddings = Embeddings
