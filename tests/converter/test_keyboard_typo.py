import random

from aisploit.converters import KeyboardTypoConverter
from aisploit.core import StringPromptValue


def test_convert_no_typo():
    converter = KeyboardTypoConverter(typo_probability=0)
    prompt = StringPromptValue(text="hello")
    assert converter.convert(prompt) == prompt


def test_convert_typo(monkeypatch):
    converter = KeyboardTypoConverter(typo_probability=1)
    monkeypatch.setattr(random, "random", lambda: 0)  # Forces a typo
    prompt = StringPromptValue(text="hello")
    assert converter.convert(prompt) != prompt


def test_convert_typo_probability_zero():
    converter = KeyboardTypoConverter(typo_probability=0)
    prompt = StringPromptValue(text="hello")
    assert converter.convert(prompt) == prompt
