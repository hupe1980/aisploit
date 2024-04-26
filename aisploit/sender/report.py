from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from ..core import BaseConverter, BasePromptValue, BaseReport, Response


@dataclass(frozen=True)
class SendReportEntry:
    prompt_value: BasePromptValue
    metadata: Dict[str, Any]
    converter: Optional[BaseConverter]
    response: Response
    start_time: datetime
    end_time: datetime

    @property
    def round_trip_time(self) -> float:
        return (self.end_time - self.start_time).total_seconds()


class SendReport(BaseReport[SendReportEntry]):
    def __init__(self, *, run_id: str) -> None:
        super().__init__(run_id=run_id)

    def has_entries(self) -> bool:
        return len(self._entries) > 0

    def add_entry(self, entry: SendReportEntry) -> None:
        self._entries.append(entry)

    def _ipython_display_(self):
        print("TODO")
