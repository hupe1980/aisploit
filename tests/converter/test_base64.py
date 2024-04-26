from aisploit.converters import Base64Converter
from aisploit.core import StringPromptValue


def test_convert_single_prompt():
    converter = Base64Converter()
    prompt = "Test"
    expected = "The following instruction is base64 encoded: VGVzdA=="
    assert converter.convert(StringPromptValue(text=prompt)).to_string() == expected


def test_convert_single_prompt_no_prefix():
    converter = Base64Converter(add_prefix=False)
    prompt = "Test"
    expected = "VGVzdA=="
    assert converter.convert(StringPromptValue(text=prompt)).to_string() == expected


def test_convert_multiple_prompts():
    converter = Base64Converter()
    prompt = "Test1"
    expected = "The following instruction is base64 encoded: VGVzdDE="
    assert converter.convert(StringPromptValue(text=prompt)).to_string() == expected


def test_convert_empty_prompt():
    converter = Base64Converter()
    prompt = ""
    expected = ""
    assert converter.convert(StringPromptValue(text=prompt)).to_string() == expected


def test_convert_with_unicode_characters():
    converter = Base64Converter()
    prompt = "äöüß"
    expected = "The following instruction is base64 encoded: w6TDtsO8w58="
    assert converter.convert(StringPromptValue(text=prompt)).to_string() == expected
