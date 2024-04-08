import os
from typing import Sequence, Optional
from pathlib import Path
from dataclasses import dataclass

from ..core.dataset import BaseDataset, YamlDeserializable


@dataclass
class Sample(YamlDeserializable):
    """A sample configuration."""

    skip: bool
    input: str
    output: str
    language: str
    tags: Sequence[str]


class SampleDataset(BaseDataset[Sample]):
    """Dataset for samples."""

    def __init__(self, samples: Sequence[Sample]) -> None:
        """Initialize the SampleDataset with a sequence of samples.

        Args:
            samples (Sequence[Sample]): The samples to initialize the dataset with.
        """
        self._entries = samples

    @classmethod
    def load_from_directory(
        cls, path: Path, tags_filter: Optional[Sequence[str]] = None
    ) -> "SampleDataset":
        """Create a SampleDataset instance by loading samples from a directory.

        Args:
            path (Path): The path to the directory containing sample YAML files.
            tags_filter (Optional[Sequence[str]], optional): Tags to filter samples. Defaults to None.

        Returns:
            SampleDataset: A dataset containing samples loaded from the directory.
        """
        samples = []
        for file_name in os.listdir(path):
            sample = Sample.from_yaml_file(path / file_name)
            if not sample.skip and (
                not tags_filter or set(sample.tags).intersection(tags_filter)
            ):
                samples.append(sample)
        return cls(samples)
