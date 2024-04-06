from typing import List
from dataclasses import dataclass

from ..core import BasePromptValue


@dataclass
class SendReportEntry:
    prompt: BasePromptValue
    response: str


class SendReport:
    entries: List[SendReportEntry]

    def __init__(self, *, run_id: str) -> None:
        self.run_id = run_id
        self.entries = []

    def has_entries(self) -> bool:
        return len(self.entries) > 0

    def add_entry(self, entry: SendReportEntry) -> None:
        self.entries.append(entry)
