import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from ..core import BasePromptValue, BaseTarget, Response


@dataclass
class OpenAIImageTarget(BaseTarget):
    api_key: Optional[str] = None

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.environ["OPENAI_API_KEY"]

        self._client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        response = self._client.images.generate(prompt=prompt.to_string(), n=1)
        print(response)
        return Response(content="")
