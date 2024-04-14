import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

from ..core import BaseConverter


class StemmingConverter(BaseConverter):
    def __init__(self) -> None:
        nltk.download("punkt", quiet=True)

    def _convert(self, prompt: str) -> str:
        words = word_tokenize(prompt)
        stemmed = [PorterStemmer().stem(w) for w in words]

        return " ".join(stemmed)
