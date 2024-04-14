from langchain_core.prompt_values import StringPromptValue

from aisploit.converters import JoinConverter


def test_join_with_default_value():
    converter = JoinConverter()
    prompt = "hello world"
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text="h-e-l-l-o w-o-r-l-d"
    )


def test_join_with_custom_value():
    converter = JoinConverter(separator="*")
    prompt = "hello world"
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text="h*e*l*l*o w*o*r*l*d"
    )


def test_join_with_empty_list():
    converter = JoinConverter()
    prompt = ""
    expected_output = ""
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(
        text=expected_output
    )
