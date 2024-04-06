from ..core import BaseConverter


class JoinConverter(BaseConverter):
    def __init__(
        self,
        *,
        separator: str = "-",
    ) -> None:
        self.separator = separator

    def _convert(self, prompt: str) -> str:
        words = prompt.split()
        joined_words = [self.separator.join(word) for word in words]
        return " ".join(joined_words)

    def __repr__(self) -> str:
        return (
            f"<{self.__module__}.{self.__class__.__name__}(separator={self.separator})>"
        )
