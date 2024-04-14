from typing import Optional
from dataclasses import dataclass
from ..core import BaseReport, BasePromptValue, Score, Response


@dataclass
class RedTeamReportEntry:
    attempt: int
    prompt: BasePromptValue
    response: Response
    score: Score


class RedTeamReport(BaseReport[RedTeamReportEntry]):
    """
    A report class for storing red team evaluation entries.
    """

    def __init__(self, *, run_id: str) -> None:
        """
        Initialize the RedTeamReport instance.

        Args:
            run_id (str): The ID of the run.
        """
        super().__init__(run_id=run_id)

    def add_entry(self, entry: RedTeamReportEntry):
        """
        Add an entry to the report.

        Args:
            entry (RedTeamReportEntry): The entry to add to the report.
        """
        self._entries.append(entry)

    @property
    def final_score(self) -> Optional[Score]:
        """
        Get the final score of the report.

        Returns:
            Optional[Score]: The final score of the report, or None if no entries exist.
        """
        if len(self._entries) == 0:
            return None
        return self._entries[-1].score

    @property
    def final_response(self) -> Optional[Response]:
        """
        Get the final response of the report.

        Returns:
            Optional[Response]: The final response of the report, or None if no entries exist.
        """
        if len(self._entries) == 0:
            return None
        return self._entries[-1].response

    def _ipython_display_(self):
        """
        Display the report in IPython environments.
        """
        print("TODO")
