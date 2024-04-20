from unittest.mock import patch

from aisploit.classifiers import PythonPackageHallucinationClassifier


@patch('requests.head')
def test_python_package_hallucination_classifier_not_flagged(mock_head):
    # Mocking the response status code
    mock_head.return_value.status_code = 200

    # Initializing the classifier
    classifier = PythonPackageHallucinationClassifier()

    # Testing with an input that contains only known packages
    input = """
import os
import zzz
from foo import bar
"""
    score = classifier.score(input)
    assert not score.flagged
    assert len(score.value) == 0

@patch('requests.head')
def test_python_package_hallucination_classifier_flagged(mock_head):
    # Mocking the response status code
    mock_head.return_value.status_code = 404

    # Initializing the classifier
    classifier = PythonPackageHallucinationClassifier()

    # Testing with an input that contains an known and unknown packages
    input = """
import os
import zzz
from foo import bar
"""
    print(input)
    score = classifier.score(input)
    assert score.flagged
    assert sorted(score.value) == sorted(["zzz", "foo"])
