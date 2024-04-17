from dataclasses import dataclass

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser

from ..core import BasePromptValue, BaseTarget, Response


@dataclass
class LangchainTarget(BaseTarget):
    model: BaseLanguageModel

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        response = self.model.invoke(prompt)

        if isinstance(response, str):
            return Response(content=response)

        if isinstance(response, BaseMessage):
            parser = StrOutputParser()
            return Response(content=parser.invoke(response))

        raise ValueError(f"Unsupported response value {type(response)}")
