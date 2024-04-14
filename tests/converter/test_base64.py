import base64

from langchain_core.prompt_values import StringPromptValue

from aisploit.converters import Base64Converter


def test_convert_single_prompt():
    converter = Base64Converter()
    prompt = "Test"
    expected_output = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text=expected_output
    )


def test_convert_multiple_prompts():
    converter = Base64Converter()
    prompt = "Test1"
    expected_output = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text=expected_output
    )


def test_convert_empty_prompt():
    converter = Base64Converter()
    prompt = ""
    expected_output = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text=expected_output
    )


def test_convert_with_unicode_characters():
    converter = Base64Converter()
    prompt = "äöüß"
    expected_output = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text=expected_output
    )
