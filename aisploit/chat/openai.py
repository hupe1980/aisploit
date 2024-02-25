from typing import Optional
from langchain_core.utils.utils import convert_to_secret_str
import langchain_openai


class ChatOpenAI(langchain_openai.ChatOpenAI):
    def __init__(
        self,
        *,
        api_key: Optional[str],
        model: str = "gpt-4",
        max_tokens: int = 1024,
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=convert_to_secret_str(api_key) if api_key else None,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
