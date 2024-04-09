from typing import Any, Generic, TypeVar, List
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from jinja2 import Template


T = TypeVar("T")


class BaseReport(Generic[T], ABC):
    """A generic base class for reports."""

    _entries: List[T]

    def __init__(self, *, run_id: str) -> None:
        """Initialize the BaseReport.

        Args:
            run_id (str): The ID of the report run.
        """
        self.run_id = run_id
        self._created_at = datetime.now()
        self._entries = []

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)
    
    def __getitem__(self, index: int) -> T:
        """Get an entry from the report by index."""
        return self._entries[index]

    @abstractmethod
    def _ipython_display_(self):
        """Display the report in IPython."""
        pass

    def _render_template(self, template_path: Path, **kwargs: Any) -> str:
        """Render the report template.

        Args:
            template_path (Path): The path to the template file.
            **kwargs (Any): Additional keyword arguments to pass to the template.

        Returns:
            str: The rendered report as a string.
        """
        with open(template_path, "r", encoding="utf8") as tpl_file:
            template = Template(tpl_file.read())
            return template.render(**kwargs)
