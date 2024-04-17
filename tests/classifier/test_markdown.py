import pytest

from aisploit.classifiers import MarkdownInjectionClassifier


@pytest.fixture
def classifier():
    return MarkdownInjectionClassifier()

def test_markdown_injection_detection_empty_input(classifier):
    score = classifier.score("")
    assert not score.flagged
    assert not score.value
    assert score.description == "Markdown Injection not detected"
    assert score.explanation == "True when a markdown injection is detected, else False"

def test_markdown_injection_detection_no_injection(classifier):
    input_text = "This is a test without any markdown injection."
    score = classifier.score(input_text)
    assert not score.flagged
    assert not score.value
    assert score.description == "Markdown Injection not detected"
    assert score.explanation == "True when a markdown injection is detected, else False"

def test_markdown_injection_detection_with_injection(classifier):
    input_text = "This is a test with ![alt_text](url) markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value
    assert score.description == "Markdown Injection detected"
    assert score.explanation == "True when a markdown injection is detected, else False"

def test_markdown_injection_detection_with_injection_with_space(classifier):
    input_text = "This is a test with ! [alt_text](url) markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value
    assert score.description == "Markdown Injection detected"
    assert score.explanation == "True when a markdown injection is detected, else False"

def test_markdown_injection_detection_with_reference_style_injection(classifier):
    input_text = "This is a test with ![alt_text][image_reference] markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value
    assert score.description == "Markdown Injection detected"
    assert score.explanation == "True when a markdown injection is detected, else False"

def test_markdown_injection_detection_with_reference_style_injection_with_space(classifier):
    input_text = "This is a test with ! [alt_text][image_reference] markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value
    assert score.description == "Markdown Injection detected"
    assert score.explanation == "True when a markdown injection is detected, else False"
