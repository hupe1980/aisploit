from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser

from ..core import BaseTarget, BasePromptValue


class LangchainTarget(BaseTarget):
    def __init__(self, *, model: BaseLanguageModel) -> None:
        self._chain = model | StrOutputParser()

    def send_prompt(self, prompt: BasePromptValue) -> str:
        return self._chain.invoke(prompt)
