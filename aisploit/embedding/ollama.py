from langchain_community.embeddings import OllamaEmbeddings as LangchainOllamaEmbeddings


from ..core import BaseEmbeddings


class OllamaEmbeddings(LangchainOllamaEmbeddings, BaseEmbeddings):
    def __init__(
        self,
        *,
        model: str = "llama2",
        **kwargs,
    ) -> None:
        super().__init__(
            model=model,
            **kwargs,
        )
