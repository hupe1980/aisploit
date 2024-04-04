import base64
import pytest
from aisploit.converter import Base64Converter


def test_convert_single_prompt():
    converter = Base64Converter()
    prompt = "Test"
    expected_output = [base64.b64encode(prompt.encode("utf-8")).decode("utf-8")]
    assert converter.convert([prompt]) == expected_output


def test_convert_multiple_prompts():
    converter = Base64Converter()
    prompts = ["Test1", "Test2", "Test3"]
    expected_output = [
        base64.b64encode(prompt.encode("utf-8")).decode("utf-8") for prompt in prompts
    ]
    assert converter.convert(prompts) == expected_output


def test_convert_empty_prompt():
    converter = Base64Converter()
    prompt = ""
    expected_output = [base64.b64encode(prompt.encode("utf-8")).decode("utf-8")]
    assert converter.convert([prompt]) == expected_output


def test_convert_with_unicode_characters():
    converter = Base64Converter()
    prompt = "äöüß"
    expected_output = [base64.b64encode(prompt.encode("utf-8")).decode("utf-8")]
    assert converter.convert([prompt]) == expected_output