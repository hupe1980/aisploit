from dataclasses import dataclass, field
from typing import Any, Dict

from langchain_core.prompt_values import PromptValue
from langchain_core.prompt_values import StringPromptValue as LangchainStringPromptValue

BasePromptValue = PromptValue
StringPromptValue = LangchainStringPromptValue


@dataclass
class Prompt:
    value: str | BasePromptValue
    metadata: Dict[str, Any] = field(default_factory=dict)
