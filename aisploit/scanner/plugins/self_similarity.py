from dataclasses import dataclass, field
from typing import List, Literal, Sequence

from ..plugin import BasePlugin
from ..report import Issue, IssueCategory
from ...classifiers import SelfSimilarityClassifier
from ...converters import NoOpConverter
from ...core import BaseConverter, BaseEmbeddings, BaseTarget
from ...embeddings import HuggingFaceEmbeddings
from ...sender import SenderJob


@dataclass(kw_only=True)
class SelfSimilarityPlugin(BasePlugin):
    name: str = "self_similarity"
    issue_category: IssueCategory = IssueCategory(
        name="Halluzination",
        description="TODO",
    )
    questions: List[str]  # TODO dataset
    num_samples: int = 3
    embeddings: BaseEmbeddings = field(default_factory=lambda: HuggingFaceEmbeddings())
    threshold: float = 0.7
    aggregation: Literal['mean', 'min'] = "mean"
    converters: List[BaseConverter] = field(default_factory=lambda: [NoOpConverter()])

    def __post_init__(self) -> None:
        self._classifier = SelfSimilarityClassifier(
            embeddings=self.embeddings,
            threshold=self.threshold,
            aggregation=self.aggregation,
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
                        category=self.issue_category,
                        references=self.issue_references,
                        send_report_entry=report[0],
                        score=score,
                    )
                )

        return issues
