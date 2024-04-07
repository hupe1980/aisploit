from langchain_community.chat_models import BedrockChat as LangchainBedrockChat

from ..core import BaseChatModel


class BedrockChat(LangchainBedrockChat, BaseChatModel):
    def __init__(
        self,
        *,
        model_id: str,
        **kwargs,
    ) -> None:
        super().__init__(
            model_id=model_id,
            **kwargs,
        )

    def supports_functions(self) -> bool:
        return False
