import textwrap
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..core import BaseChatModelConverter, BaseChatModel

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


class GenderConverter(BaseChatModelConverter):
    def __init__(self, *, chat_model: BaseChatModel, prompt=_template) -> None:
        super().__init__(chat_model)
        self._chain = prompt | chat_model | StrOutputParser()

    def _convert(self, prompt: str) -> str:
        return self._chain.invoke({"input": prompt})
