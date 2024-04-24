from langchain_community.embeddings import (
    HuggingFaceEmbeddings as LangchainHuggingFaceEmbeddings,
)

from ..core import BaseEmbeddings


class HuggingFaceEmbeddings(LangchainHuggingFaceEmbeddings, BaseEmbeddings):
    def __init__(
        self,
        *,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        **kwargs,
    ) -> None:
        super().__init__(
            model_name=model_name,
            **kwargs,
        )
