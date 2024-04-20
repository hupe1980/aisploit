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
        Swap the gender in the given text.
        Input text:
        {input}

        Instructions:
        1. Identify gender-specific terms such as pronouns (e.g., he, she), names, titles, and other gendered language in the input text.
        2. Replace the identified gender-specific terms with their gender-swapped counterparts. For example:
            - Replace "he" with "she" and vice versa.
            - Replace male names with female names and vice versa.
            - Adjust any associated verbs, adjectives, or other language to maintain grammatical correctness.
        3. Ensure that the gender-swapped text retains the original context and meaning as much as possible.
        """
    )
)


@dataclass
class GenderConverter(BaseChatModelConverter):
    prompt: ChatPromptTemplate = field(default_factory=lambda: _template)
    _chain: RunnableSerializable[Dict, str] = field(init=False)

    def __post_init__(self) -> None:
        self._chain = self.prompt | self.chat_model | StrOutputParser()

    def _convert(self, prompt: str) -> str:
        return self._chain.invoke({"input": prompt})
