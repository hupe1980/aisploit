import abc
import os
import yaml
from pathlib import Path
from typing import Generic, Type, TypeVar, Sequence
from dataclasses import dataclass

T = TypeVar("T")


class YamlDeserializable(abc.ABC):
    @classmethod
    def from_yaml_file(cls: Type[T], file: Path) -> T:
        # Check if file exists before reading
        if not file.exists():
            raise FileNotFoundError(f"File '{file}' does not exist.")

        with open(file, "r", encoding="utf-8") as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(f"Invalid YAML file '{file}': {exc}")

        data_object = cls(**yaml_data)
        return data_object


@dataclass
class Prompt(YamlDeserializable):
    name: str
    skip: bool
    source: str
    language: str
    tags: Sequence[str]
    parameters: Sequence[str]
    template: str


JAILBREAK_PROMPTS_PATH = Path(__file__, "..", "jailbreak").resolve()


class Dataset(Generic[T]):
    _prompts: Sequence[T]

    def __iter__(self):
        return iter(self._prompts)

    def __len__(self):
        return len(self._prompts)


class JailbreakDataset(Dataset[Prompt]):
    def __init__(
        self,
        *,
        path=JAILBREAK_PROMPTS_PATH,
    ) -> None:
        self._prompts = []
        for file_name in os.listdir(path):
            prompt = Prompt.from_yaml_file(path / file_name)
            if not prompt.skip:
                self._prompts.append(prompt)
