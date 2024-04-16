from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from .plugin import Plugin
from .plugins import PromptInjectionPlugin
from .report import Issue, ScanReport
from ..core import BaseJob, BaseTarget, CallbackManager, Callbacks


@dataclass
class ScannerJob(BaseJob):
    target: BaseTarget
    plugins: Sequence[Plugin] = field(default_factory=lambda: [PromptInjectionPlugin(name="prompt_injection")])
    callbacks: Callbacks = field(default_factory=list)

    def execute(self, *, run_id: Optional[str] = None, tags: Optional[Sequence[str]] = None) -> ScanReport:
        run_id = run_id or self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self.callbacks,
        )

        issues: List[Issue] = []
        for plugin in self.plugins:
            callback_manager.on_scanner_plugin_start(plugin.name)
            plugin_issues = plugin.run(run_id=run_id, target=self.target)
            callback_manager.on_scanner_plugin_end(plugin.name)
            issues.extend(plugin_issues)

        return ScanReport(
            run_id=run_id,
            issues=issues,
        )
