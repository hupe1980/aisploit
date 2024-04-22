from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Sequence

from .report import Issue, IssueCategory
from ..converters import NoOpConverter
from ..core import BaseConverter, BasePromptValue, BaseTarget, BaseTextClassifier
from ..sender import SenderJob


@dataclass
class Plugin(ABC):
    name: str

    @abstractmethod
    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        pass


@dataclass(kw_only=True)
class SendPromptsPlugin(Plugin, ABC):
    converters: List[BaseConverter] = field(default_factory=lambda: [NoOpConverter()])
    issue_category: IssueCategory
    issue_references: Sequence[str] = field(default_factory=list)
    classifier: BaseTextClassifier

    @abstractmethod
    def create_prompts(self) -> Sequence[str | BasePromptValue]:
        pass

    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        sender = SenderJob(
            target=target,
            converters=self.converters,
            include_original_prompt=True,
            disable_progressbar=True,
        )

        report = sender.execute(
            run_id=run_id,
            prompts=self.create_prompts(),
        )

        issues: List[Issue] = []

        for entry in report:
            score = self.classifier.score(entry.response.content)
            if score.flagged:
                issues.append(
                    Issue(
                        category=self.issue_category,
                        references=self.issue_references,
                        send_report_entry=entry,
                        score=score,
                    )
                )

        return issues
