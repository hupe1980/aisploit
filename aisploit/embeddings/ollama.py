from langchain_community.embeddings import OllamaEmbeddings as LangchainOllamaEmbeddings


class OllamaEmbeddings(LangchainOllamaEmbeddings):
    def __init__(
        self,
        *,
        model: str = "llama2",
        **kwargs,
    ) -> None:
        super().__init__(
            model=model,
        )
