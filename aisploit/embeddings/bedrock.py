from langchain_community.embeddings import (
    BedrockEmbeddings as LangchainBedrockEmbeddings,
)

from ..core import BaseEmbeddings


class BedrockEmbeddings(LangchainBedrockEmbeddings, BaseEmbeddings):
    def __init__(
        self,
        *,
        model_id: str = "amazon.titan-embed-text-v1",
        **kwargs,
    ) -> None:
        super().__init__(
            model_id=model_id,
            **kwargs,
        )
