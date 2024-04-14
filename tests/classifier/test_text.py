import re
import pytest
from aisploit.classifiers import RegexClassifier, SubstringClassifier


@pytest.fixture
def regex_classifier():
    pattern = re.compile(r"\btest\b")  # Example regex pattern
    return RegexClassifier(pattern=pattern)


@pytest.fixture
def substring_finder_classifier():
    substring = "test"  # Example substring
    return SubstringClassifier(substring=substring)


def test_regex_classifier_score_text_match(regex_classifier):
    text = "This is a test text"
    score = regex_classifier.score(text)
    assert score.value is True
    assert (
        score.description
        == f"Return True if the pattern \\btest\\b is found in the input"
    )


def test_regex_classifier_score_text_no_match(regex_classifier):
    text = "This is not a matching text"
    score = regex_classifier.score(text)
    assert score.value is False
    assert (
        score.description
        == f"Return True if the pattern \\btest\\b is found in the input"
    )


def test_substring_finder_classifier_score_text_match(substring_finder_classifier):
    text = "This is a test text"
    score = substring_finder_classifier.score(text)
    assert score.value is True
    assert score.description == f"Return True if the pattern test is found in the input"


def test_substring_finder_classifier_score_text_no_match(substring_finder_classifier):
    text = "This is not a matching text"
    score = substring_finder_classifier.score(text)
    assert score.value is False
    assert score.description == f"Return True if the pattern test is found in the input"
