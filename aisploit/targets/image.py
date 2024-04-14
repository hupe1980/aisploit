from typing import Optional
import os
from openai import OpenAI
from ..core import BaseTarget, Response, BasePromptValue


class ImageTarget(BaseTarget):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
    ) -> None:
        if not api_key:
            api_key = os.environ["OPENAI_API_KEY"]

        self._client = OpenAI(api_key=api_key)

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        response = self._client.images.generate(prompt=prompt.to_string(), n=1)
        print(response)
        return Response(content="")
