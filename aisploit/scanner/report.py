from typing import List

from .issue import Issue


class ScanReport:
    def __init__(
        self,
        *,
        run_id: str,
        issues: List[Issue] = [],
    ) -> None:
        self.run_id = run_id
        self.issues = issues

    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def _ipython_display_(self):
        for issue in self.issues:
            print(f"Category: {issue.category}")
            print(f"Description: {issue.description}")
