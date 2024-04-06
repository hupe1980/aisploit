from typing import Any, Dict, Optional, Sequence, List
from uuid import uuid4


from ..core import BaseJob, BaseTarget, Callbacks, CallbackManager
from .plugins import PromptInjectionPlugin
from .plugin import Plugin, PluginRegistry
from .issue import Issue
from .report import ScanReport

PluginRegistry.register("prompt_injection", PromptInjectionPlugin, tags=["jailbreak"])


class ScannerJob(BaseJob):
    def __init__(
        self,
        *,
        target: BaseTarget,
        plugin_params: Dict[str, Any] = {},
        callbacks: Callbacks = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)

        self.scan_id = str(uuid4())
        self._target = target
        self._plugin_params = plugin_params
        self._callbacks = callbacks

    def execute(
        self, *, run_id: Optional[str] = None, tags: Optional[Sequence[str]] = None
    ) -> ScanReport:
        if not run_id:
            run_id = self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self._callbacks,
        )

        issues: List[Issue] = []
        for name, plugin in self.get_plugin(tags=tags).items():
            callback_manager.on_scanner_plugin_start(name)
            plugin_issues = plugin.run(self._target)
            callback_manager.on_scanner_plugin_end(name)
            issues.extend(plugin_issues)

        return ScanReport(
            run_id=run_id,
            issues=issues,
        )

    def get_plugin(self, tags: Optional[Sequence[str]] = None) -> Dict[str, Plugin]:
        plugins = {}
        classes = PluginRegistry.get_plugin_classes(tags=tags)

        for name, plugin_cls in classes.items():
            kwargs = self._plugin_params.get(name, {})
            plugins[name] = plugin_cls(**kwargs)

        return plugins
