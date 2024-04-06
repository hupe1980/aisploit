from langchain_core.prompt_values import StringPromptValue
from aisploit.converter import JoinConverter

def test_join_with_default_value():
    converter = JoinConverter()
    prompt = "hello world"
    expected_output = converter.join_value.join(prompt)
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(text=expected_output)

def test_join_with_custom_value():
    converter = JoinConverter(join_value="_")
    prompt = "hello world"
    expected_output = "_".join(prompt)
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(text=expected_output)

def test_join_with_empty_list():
    converter = JoinConverter()
    prompt = ""
    expected_output = ""
    assert converter.convert(StringPromptValue(text=prompt)) == StringPromptValue(text=expected_output)
