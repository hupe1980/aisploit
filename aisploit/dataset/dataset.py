import abc
import os
import yaml
from pathlib import Path
from typing import Generic, Type, TypeVar, Sequence
from dataclasses import dataclass

T = TypeVar("T")


class YamlDeserializable(abc.ABC):
    """Abstract base class for objects that can be deserialized from YAML."""

    @classmethod
    def from_yaml_file(cls: Type[T], file: Path) -> T:
        """Load an object from a YAML file.

        Args:
            cls (Type[T]): The class to instantiate.
            file (Path): The path to the YAML file.

        Returns:
            T: An instance of the class deserialized from the YAML file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If there's an error in parsing the YAML data.
        """
        # Check if file exists before reading
        if not file.exists():
            raise FileNotFoundError(f"File '{file}' does not exist.")

        with open(file, "r", encoding="utf-8") as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(f"Invalid YAML file '{file}': {exc}")

        return cls(**yaml_data)


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


JAILBREAK_PROMPTS_PATH = Path(__file__, "..", "jailbreak").resolve()


class Dataset(Generic[T]):
    """Generic dataset class."""

    _prompts: Sequence[T]

    def __iter__(self):
        return iter(self._prompts)

    def __len__(self):
        return len(self._prompts)


class JailbreakDataset(Dataset[Prompt]):
    """Dataset for jailbreak prompts."""

    def __init__(
        self,
        *,
        path=JAILBREAK_PROMPTS_PATH,
    ) -> None:
        """Initialize the JailbreakDataset.

        Args:
            path (str): The path to the directory containing prompt YAML files.
        """
        self._prompts = []
        for file_name in os.listdir(path):
            prompt = Prompt.from_yaml_file(path / file_name)
            if not prompt.skip:
                self._prompts.append(prompt)
