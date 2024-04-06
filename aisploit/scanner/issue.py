from typing import Sequence
from dataclasses import dataclass

from ..core import BaseConverter, BasePromptValue


@dataclass(frozen=True)
class IssueCategory:
    name: str
    description: str


@dataclass
class Issue:
    category: IssueCategory
    references: Sequence[str]
    prompt: BasePromptValue
    converter: BaseConverter
    response: str
