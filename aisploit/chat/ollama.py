from langchain_community.chat_models import ChatOllama as LangchainChatOllama


class ChatOllama(LangchainChatOllama):
    def __init__(
        self,
        *,
        model: str = "llama2",
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        super().__init__(
            model=model,
            temperature=temperature,
            **kwargs,
        )
