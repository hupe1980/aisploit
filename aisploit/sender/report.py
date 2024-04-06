from typing import List
from dataclasses import dataclass

from ..core import BasePromptValue, BaseReport, BaseConverter


@dataclass
class SendReportEntry:
    prompt: BasePromptValue
    converter: BaseConverter
    response: str


class SendReport(BaseReport):
    entries: List[SendReportEntry]

    def __init__(self, *, run_id: str) -> None:
        super().__init__(run_id=run_id)
        self.entries = []

    def has_entries(self) -> bool:
        return len(self.entries) > 0

    def add_entry(self, entry: SendReportEntry) -> None:
        self.entries.append(entry)

    def _ipython_display_(self):
        print("TODO")
