from aisploit.converter import KeyboardTypoConverter

# Test data
test_prompts = ["Hello", "World", "QWERTY"]
random_state = 42

# Test conversion with default parameters
def test_convert_with_default_params():
    converter = KeyboardTypoConverter(random_state=random_state)
    converted_prompts = converter.convert(test_prompts)
    assert len(converted_prompts) == len(test_prompts)
    for prompt, converted_prompt in zip(test_prompts, converted_prompts):
        assert len(prompt) == len(converted_prompt)
        assert prompt != converted_prompt

# Test conversion with custom typo probability
def test_convert_with_custom_typo_probability():
    typo_probability = 0.0
    converter = KeyboardTypoConverter(typo_probability=typo_probability, random_state=random_state)
    converted_prompts = converter.convert(test_prompts)
    assert len(converted_prompts) == len(test_prompts)
    for prompt, converted_prompt in zip(test_prompts, converted_prompts):
        assert len(prompt) == len(converted_prompt)
        assert prompt == converted_prompt

# Test conversion with custom keyboard neighbors
def test_convert_with_custom_keyboard_neighbors():
    custom_keyboard_neighbors = {
        'q': ['w'],
        'w': ['q', 'e'],
        'e': ['w', 'r'],
        'r': ['e', 't'],
        't': ['r', 'y'],
        'y': ['t', 'u'],
        'u': ['y', 'i'],
        'i': ['u', 'o'],
        'o': ['i', 'p'],
        'p': ['o'],
        'l': ['k'],
    }
    converter = KeyboardTypoConverter(keyboard_neighbors=custom_keyboard_neighbors, random_state=random_state)
    converted_prompts = converter.convert(test_prompts)
    assert len(converted_prompts) == len(test_prompts)
    for prompt, converted_prompt in zip(test_prompts, converted_prompts):
        assert len(prompt) == len(converted_prompt)
        assert prompt != converted_prompt