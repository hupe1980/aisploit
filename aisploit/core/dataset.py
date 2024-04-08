from abc import ABC
import yaml
from pathlib import Path
from typing import Generic, Type, TypeVar, Sequence

T = TypeVar("T")


class BaseDataset(Generic[T]):
    """Generic dataset class."""

    _entries: Sequence[T]

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)


class YamlDeserializable(ABC):
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
