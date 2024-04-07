from typing import List, Optional
from dataclasses import dataclass
from ..core import BaseReport, BasePromptValue, Score


@dataclass
class RedTeamReportEntry:
    attempt: int
    prompt: BasePromptValue
    response: str
    score: Score


class RedTeamReport(BaseReport[RedTeamReportEntry]):
    def __init__(self, *, run_id: str) -> None:
        super().__init__(run_id=run_id)

    def add_entry(self, entry: RedTeamReportEntry):
        self._entries.append(entry)

    @property
    def final_score(self) -> Optional[Score]:
        last_entry = self._entries[-1]
        if last_entry:
            return last_entry.score
        return None

    def _ipython_display_(self):
        print("TODO")
