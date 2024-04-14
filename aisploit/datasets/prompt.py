import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

from ..core.dataset import BaseDataset, YamlDeserializable


@dataclass
class Prompt(YamlDeserializable):
    """A prompt configuration."""

    name: str
    skip: bool
    source: str
    language: str
    tags: Sequence[str]
    parameters: Sequence[str]
    template: str


class PromptDataset(BaseDataset[Prompt]):
    """Dataset for prompts."""

    def __init__(self, prompts: Sequence[Prompt]) -> None:
        """Initialize the PromptDataset with a sequence of prompts.

        Args:
            prompts (Sequence[Prompt]): The prompts to initialize the dataset with.
        """
        self._entries = prompts

    @classmethod
    def load_from_directory(cls, path: Path, tags_filter: Optional[Sequence[str]] = None) -> "PromptDataset":
        """Create a JailbreakDataset instance by loading prompts from a directory.

        Args:
            path (Path): The path to the directory containing prompt YAML files.
            tags_filter (Sequence[str], optional): Tags to filter prompts. Defaults to None.

        Returns:
            JailbreakDataset: A dataset containing prompts loaded from the directory.
        """
        prompts = []
        for file_name in os.listdir(path):
            prompt = Prompt.from_yaml_file(path / file_name)
            if not prompt.skip and (not tags_filter or set(prompt.tags).intersection(tags_filter)):
                prompts.append(prompt)
        return cls(prompts)


JailbreakPromptDataset = PromptDataset.load_from_directory(
    Path(__file__, "..", "prompts").resolve(), tags_filter=["jailbreak"]
)
