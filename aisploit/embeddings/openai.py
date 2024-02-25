from typing import Optional
from langchain_core.utils.utils import convert_to_secret_str
import langchain_openai


class OpenAIEmbeddings(langchain_openai.OpenAIEmbeddings):
    def __init__(
        self,
        *,
        api_key: Optional[str],
        model: str = "text-embedding-ada-002",
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            **kwargs,
        )
