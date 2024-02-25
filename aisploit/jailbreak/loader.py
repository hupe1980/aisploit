import pathlib
import yaml
from langchain_core.prompts import PromptTemplate

PROMPTS_PATH = pathlib.Path(__file__, "..", "prompts").resolve()


class JailbreakPromptTemplate(PromptTemplate):
    id: str
    name: str


def load_jailbreak_prompt(id: str) -> JailbreakPromptTemplate:
    prompt_file = PROMPTS_PATH / f"{id}.yaml"
    if not prompt_file.exists():
        raise FileNotFoundError(f"File '{prompt_file}' does not exist.")

    try:
        yaml_data = yaml.safe_load(prompt_file.read_text("utf-8"))
    except yaml.YAMLError as err:
        raise ValueError(f"Invalid YAML file '{prompt_file}': {err}")

    return JailbreakPromptTemplate(
        id=yaml_data.get("id"),
        name=yaml_data.get("name"),
        template=yaml_data.get("template"),
        input_variables=yaml_data.get("input_variables", []),
    )
