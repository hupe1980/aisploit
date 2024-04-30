from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, Sequence, Type, TypeVar

import yaml
from pandas import DataFrame

T = TypeVar("T")


class BaseDataset(ABC):
    """Generic dataset class."""

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass


class DataclassDataset(BaseDataset, Generic[T]):
    """Dataset class based on dataclasses."""

    _entries: Sequence[T]

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)


class TabularDataset(BaseDataset):
    """Dataset class for tabular data."""

    _df: DataFrame

    def __iter__(self):
        for row in self._df.values.tolist():
            yield row

    def __len__(self):
        return len(self._df)


class YamlDeserializable:
    """Base class for objects that can be deserialized from YAML."""

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
                raise ValueError(f"Invalid YAML file '{file}'") from exc

        return cls(**yaml_data)
