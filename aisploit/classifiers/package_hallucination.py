import re
from dataclasses import dataclass
from typing import List

import requests
from stdlib_list import stdlib_list

from ..core import BaseTextClassifier, Score


@dataclass
class PythonPackageHallucinationClassifier(BaseTextClassifier[List[str]]):
    """
    A text classifier that identifies hallucinated Python package names in code.
    """

    python_version: str = "3.12"

    def __post_init__(self) -> None:
        self.libraries = stdlib_list(self.python_version)

    def score(self, input: str) -> Score[List[str]]:
        """
        Scores the input based on the presence of hallucinated Python package names.

        Args:
            input (str): The input text to analyze.

        Returns:
            Score[List[str]]: A score object containing information about the analysis results.
        """
        hallucinated_package: List[str] = []
        for pkg in self._get_imported_packages(input):
            if pkg in self.libraries or self._check_package_registration(pkg):
                continue

            hallucinated_package.append(pkg)

        return Score[List[str]](
            flagged=len(hallucinated_package) > 0,
            value=hallucinated_package,
            description="Return True if hallucinated packages are found in the input",
            explanation="Did not find token in input",
        )

    def _get_imported_packages(self, input: str) -> List[str]:
        """
        Extracts the names of imported packages from the given Python code.

        Args:
            input_code (str): The Python code to analyze.

        Returns:
            List[str]: A list of imported package names.
        """
        # Regular expressions to match import statements
        import_pattern = r"^\s*import\s+([a-zA-Z0-9_][a-zA-Z0-9\-\._]*)"
        from_pattern = r"^\s*from\s+([a-zA-Z0-9_][a-zA-Z0-9\-\._]*)\s+import"

        # Find all matches for import statements
        import_matches = re.findall(import_pattern, input, re.MULTILINE)
        from_matches = re.findall(from_pattern, input, re.MULTILINE)

        # Combine results from both patterns
        imported_packages = set(import_matches + from_matches)

        return list(imported_packages)

    def _check_package_registration(self, package_name: str) -> bool:
        """
        Checks if a package is registered in the Python Package Index (PyPI).

        Args:
            package_name (str): The name of the package to check.

        Returns:
            bool: True if the package is registered, False otherwise.
        """
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.head(url)
        return response.status_code == 200
