from typing import Union
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable


BaseLLM = Runnable[LanguageModelInput, str]

BaseChatModel = Runnable[LanguageModelInput, BaseMessage]

BaseModel = Union[BaseLLM, BaseChatModel]
