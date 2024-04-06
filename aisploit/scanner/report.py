from typing import List

from .issue import Issue


class ScanReport:
    def __init__(
        self,
        *,
        issues: List[Issue] = [],
    ) -> None:
        self.issues = issues

    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def _ipython_display_(self):
        print("TODO ScanReport")
