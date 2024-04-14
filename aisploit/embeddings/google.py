from typing import Optional

from langchain_core.utils.utils import convert_to_secret_str
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings as LangchainGoogleGenerativeAIEmbeddings,
)

from ..core import BaseEmbeddings


class GoogleGenerativeAIEmbeddings(LangchainGoogleGenerativeAIEmbeddings, BaseEmbeddings):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "models/embedding-001",
        **kwargs,
    ) -> None:
        super().__init__(
            google_api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            **kwargs,
        )
