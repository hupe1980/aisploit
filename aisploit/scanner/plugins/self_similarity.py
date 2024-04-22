from dataclasses import dataclass, field
from typing import List, Sequence

from ..plugin import Plugin
from ..report import Issue, IssueCategory
from ...classifiers import SelfSimilarityClassifier
from ...converters import NoOpConverter
from ...core import BaseConverter, BaseTarget
from ...sender import SenderJob


@dataclass(kw_only=True)
class SelfSimilarityPlugin(Plugin):
    questions: List[str]  # TODO dataset
    num_samples: int = 3
    model_name_or_path: str = "all-MiniLM-L6-v2"
    threshold: float = 0.7
    converters: List[BaseConverter] = field(default_factory=lambda: [NoOpConverter()])
    name: str = field(default="self_similarity", init=False)

    def __post_init__(self) -> None:
        self._classifier = SelfSimilarityClassifier(
            model_name_or_path=self.model_name_or_path,
            threshold=self.threshold,
        )

    def run(self, *, run_id: str, target: BaseTarget) -> Sequence[Issue]:
        issues: List[Issue] = []

        for question in self.questions:
            sender = SenderJob(
                target=target,
                include_original_prompt=True,
                disable_progressbar=True,
            )

            report = sender.execute(
                run_id=run_id,
                prompts=[question],
            )

            proof_sender = SenderJob(
                target=target,
                converters=self.converters,
                include_original_prompt=True,
                disable_progressbar=True,
            )

            proof_report = proof_sender.execute(
                run_id=run_id,
                prompts=[question] * self.num_samples,
            )

            references = [entry.response.content for entry in proof_report]
            print(report[0].response.content, references)
            score = self._classifier.score(report[0].response.content, references=references)
            print(score)
            if score.flagged:
                issues.append(
                    Issue(
                        category=IssueCategory(
                            name="Halluzination",
                            description="TODO",
                        ),
                        references=[],
                        send_report_entry=report[0],
                        score=score,
                    )
                )

        return issues
