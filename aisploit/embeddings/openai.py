from typing import Optional
from langchain_core.utils.utils import convert_to_secret_str
from langchain_openai import OpenAIEmbeddings as LangchainOpenAIEmbeddings


from ..core import BaseEmbeddings


class OpenAIEmbeddings(LangchainOpenAIEmbeddings, BaseEmbeddings):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "text-embedding-ada-002",
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            **kwargs,
        )
