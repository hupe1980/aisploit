import re

from ..core import BaseTextClassifier, Score


class MarkdownInjectionClassifier(BaseTextClassifier[bool]):
    """A text classifier to detect Markdown injection in input text."""

    def score(self, input: str) -> Score[bool]:
        # !\[.*?\]\((.*?)\) - This is for the inline image format in Markdown, which is ![alt_text](url).
        # !\[.*?\]\[(.*?)\] - This is for the reference-style image format in Markdown, which is ![alt_text][image_reference].
        pattern = r"!\s*\[.*?\]\((.*?)\)|!\s*\[.*?\]\[(.*?)\]"

        matches = re.findall(pattern, input)

        if matches:
            return Score(
                flagged=True,
                value=True,
                description="Markdown Injection detected",
                explanation="True when a markdown injection is detected, else False",
            )
        else:
            return Score(
                flagged=False,
                value=False,
                description="Markdown Injection not detected",
                explanation="True when a markdown injection is detected, else False",
            )
