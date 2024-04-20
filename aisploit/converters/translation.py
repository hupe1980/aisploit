import textwrap
from dataclasses import dataclass, field
from typing import Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from ..core import BaseChatModelConverter

_template = ChatPromptTemplate.from_template(
    textwrap.dedent(
        """
        Translate the following text to {language}.
        Please maintain the original meaning and context as closely as possible.

        Input text:
        {input}

        Translated text:
        """
    )
)


@dataclass
class TranslationConverter(BaseChatModelConverter):
    language: str
    prompt: ChatPromptTemplate = field(default_factory=lambda: _template)
    _chain: RunnableSerializable[Dict, str] = field(init=False)

    def __post_init__(self) -> None:
        self._chain = self.prompt | self.chat_model | StrOutputParser()

    def _convert(self, prompt: str) -> str:
        return self._chain.invoke({"input": prompt, "language": self.language})
