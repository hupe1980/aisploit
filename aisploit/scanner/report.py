from typing import List, Sequence
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from IPython.display import display_markdown

from ..core import BaseReport
from ..sender import SendReportEntry


TEMPLATES_PATH = Path(__file__, "..", "templates").resolve()


@dataclass(frozen=True)
class IssueCategory:
    name: str
    description: str


@dataclass
class Issue:
    category: IssueCategory
    references: Sequence[str]
    send_report_entry: SendReportEntry


class ScanReport(BaseReport[Issue]):
    def __init__(
        self,
        *,
        run_id: str,
        issues: List[Issue] = [],
    ) -> None:
        super().__init__(run_id=run_id)
        self._issues = issues

    def has_issues(self) -> bool:
        return len(self._issues) > 0

    def to_markdown(self, *, template_path=TEMPLATES_PATH / "report.md") -> str:
        issues_by_category = defaultdict[IssueCategory, List[Issue]](list)
        for issue in self._issues:
            issues_by_category[issue.category].append(issue)

        return self._render_template(
            template_path=template_path,
            run_id=self.run_id,
            created_at=self.created_at,
            issues_by_category=issues_by_category,
        )

    def _ipython_display_(self):
        markdown = self.to_markdown()
        display_markdown(markdown, raw=True)
