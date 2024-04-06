from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path
from jinja2 import Template


class BaseReport(ABC):
    def __init__(self, *, run_id: str) -> None:
        self.run_id = run_id

    @abstractmethod
    def _ipython_display_(self):
        pass

    def _render_template(self, template_path: Path, **kwargs: Any) -> str:
        with open(template_path, "r", encoding="utf8") as tpl_file:
            template = Template(tpl_file.read())
            return template.render(**kwargs)
