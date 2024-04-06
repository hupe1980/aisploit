from ..core import BaseConverter


class JoinConverter(BaseConverter):
    def __init__(
        self,
        *,
        join_value: str = "-",
    ) -> None:
        self.join_value = join_value

    def _convert(self, prompt: str) -> str:
        return self.join_value.join(prompt)
