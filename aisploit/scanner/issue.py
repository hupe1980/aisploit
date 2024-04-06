from typing import Sequence
from dataclasses import dataclass


@dataclass
class Issue:
    category: str
    description: str
    references: Sequence[str]
