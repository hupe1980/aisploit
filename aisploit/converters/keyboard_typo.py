import random

from ..core import BaseConverter

KEYBOARD_NEIGHBORS_QWERTZ = {
    "q": ["w", "a", "s"],
    "w": ["q", "e", "s", "d"],
    "e": ["w", "r", "d", "f"],
    "r": ["e", "t", "f", "g"],
    "t": ["r", "z", "g", "h"],
    "z": ["t", "u", "h", "j"],
    "u": ["z", "i", "j", "k"],
    "i": ["u", "o", "k", "l"],
    "o": ["i", "p", "l"],
    "a": ["q", "s", "y"],
    "s": ["a", "w", "e", "d", "x", "y"],
    "d": ["s", "e", "r", "f", "c", "x"],
    "f": ["d", "r", "t", "g", "v", "c"],
    "g": ["f", "t", "z", "h", "b", "v"],
    "h": ["g", "z", "u", "j", "n", "b"],
    "j": ["h", "u", "i", "k", "m", "n"],
    "k": ["j", "i", "o", "l", "m"],
    "l": ["k", "o", "p"],
    "y": ["a", "s", "x"],
    "x": ["z", "s", "d", "c"],
    "c": ["x", "d", "f", "v"],
    "v": ["c", "f", "g", "b"],
    "b": ["v", "g", "h", "n"],
    "n": ["b", "h", "j", "m"],
    "m": ["n", "j", "k"],
}

KEYBOARD_NEIGHBORS_QWERTY = {
    "q": ["w", "a", "s"],
    "w": ["q", "a", "s", "d", "e"],
    "e": ["w", "s", "d", "f", "r"],
    "r": ["e", "d", "f", "g", "t"],
    "t": ["r", "f", "g", "h", "y"],
    "y": ["t", "g", "h", "j", "u"],
    "u": ["y", "h", "j", "k", "i"],
    "i": ["u", "j", "k", "l", "o"],
    "o": ["i", "k", "l", "p"],
    "p": ["o", "l"],
    "a": ["q", "w", "s", "z"],
    "s": ["q", "w", "e", "a", "d", "z", "x"],
    "d": ["w", "e", "r", "s", "f", "x", "c"],
    "f": ["e", "r", "t", "d", "g", "c", "v"],
    "g": ["r", "t", "y", "f", "h", "v", "b"],
    "h": ["t", "y", "u", "g", "j", "b", "n"],
    "j": ["y", "u", "i", "h", "k", "n", "m"],
    "k": ["u", "i", "o", "j", "l", "m"],
    "l": ["i", "o", "p", "k"],
    "z": ["a", "s", "x"],
    "x": ["z", "s", "d", "c"],
    "c": ["x", "d", "f", "v"],
    "v": ["c", "f", "g", "b"],
    "b": ["v", "g", "h", "n"],
    "n": ["b", "h", "j", "m"],
    "m": ["n", "j", "k"],
}


class KeyboardTypoConverter(BaseConverter):
    def __init__(
        self,
        *,
        keyboard_neighbors=KEYBOARD_NEIGHBORS_QWERTY,
        typo_probability=0.1,
        random_state=None,
    ) -> None:
        self._keyboard_neighbors = keyboard_neighbors
        self._typo_probability = typo_probability
        if random_state is not None:
            random.seed(random_state)

    def _convert(self, prompt: str) -> str:
        typoPrompt = ""
        for char in prompt:
            if random.random() < self._typo_probability and char.lower() in self._keyboard_neighbors:
                # Replace the character with a random neighboring key
                neighbor_keys = self._keyboard_neighbors[char.lower()]
                typo_char = random.choice(neighbor_keys)
                # Preserve the original case
                if char.isupper():
                    typo_char = typo_char.upper()
                char = typo_char
            typoPrompt += char

        return typoPrompt
