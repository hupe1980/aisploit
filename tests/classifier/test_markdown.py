import pytest

from aisploit.classifiers import MarkdownInjectionClassifier


@pytest.fixture
def classifier():
    return MarkdownInjectionClassifier()


def test_markdown_injection_detection_empty_input(classifier):
    score = classifier.score("")
    assert not score.flagged
    assert score.value == []
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection not detected"


def test_markdown_injection_detection_no_injection(classifier):
    input_text = "This is a test without any markdown injection."
    score = classifier.score(input_text)
    assert not score.flagged
    assert score.value == []
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection not detected"


def test_markdown_injection_detection_with_injection(classifier):
    input_text = "This is a test with ![alt_text](url) markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value == [('url', '')]
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection detected"


def test_markdown_injection_detection_with_injection_with_space(classifier):
    input_text = "This is a test with ! [alt_text](url) markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value == [('url', '')]
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection detected"


def test_markdown_injection_detection_with_reference_style_injection(classifier):
    input_text = "This is a test with ![alt_text][image_reference] markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value == [('', 'image_reference')]
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection detected"


def test_markdown_injection_detection_with_reference_style_injection_with_space(classifier):
    input_text = "This is a test with ! [alt_text][image_reference] markdown injection."
    score = classifier.score(input_text)
    assert score.flagged
    assert score.value == [('', 'image_reference')]
    assert score.description == "Returns True if a markdown injection is detected, else False."
    assert score.explanation == "Markdown Injection detected"
