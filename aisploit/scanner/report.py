from typing import List
from collections import defaultdict
from pathlib import Path
from IPython.display import display_markdown

from ..core import BaseReport
from .issue import Issue, IssueCategory


TEMPLATES_PATH = Path(__file__, "..", "templates").resolve()


class ScanReport(BaseReport):
    def __init__(
        self,
        *,
        run_id: str,
        issues: List[Issue] = [],
    ) -> None:
        super().__init__(run_id=run_id)
        self.issues = issues

    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def to_markdown(self, *, template_path=TEMPLATES_PATH / "report.md") -> str:
        issues_by_category = defaultdict[IssueCategory, List[Issue]](list)
        for issue in self.issues:
            issues_by_category[issue.category].append(issue)

        return self._render_template(
            template_path=template_path,
            run_id=self.run_id,
            report=self,
            issues_by_category=issues_by_category,
        )

    def _ipython_display_(self):
        markdown = self.to_markdown()
        display_markdown(markdown, raw=True)
