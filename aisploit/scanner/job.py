from typing import Optional, Sequence, List

from ..core import BaseJob, BaseTarget, Callbacks, CallbackManager
from .plugins import PromptInjectionPlugin
from .plugin import Plugin
from .report import ScanReport, Issue


class ScannerJob(BaseJob):
    def __init__(
        self,
        *,
        target: BaseTarget,
        plugins: Sequence[Plugin] = [PromptInjectionPlugin()],
        callbacks: Callbacks = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)

        self._target = target
        self._plugins = plugins
        self._callbacks = callbacks

    def execute(
        self, *, run_id: Optional[str] = None, tags: Optional[Sequence[str]] = None
    ) -> ScanReport:
        run_id = run_id or self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self._callbacks,
        )

        issues: List[Issue] = []
        for plugin in self._plugins:
            callback_manager.on_scanner_plugin_start(plugin.name)
            plugin_issues = plugin.run(run_id=run_id, target=self._target)
            callback_manager.on_scanner_plugin_end(plugin.name)
            issues.extend(plugin_issues)

        return ScanReport(
            run_id=run_id,
            issues=issues,
        )
