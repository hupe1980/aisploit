from typing import Union, Sequence, Optional
from langchain_core.prompt_values import StringPromptValue
from ..core import BaseJob, BaseConverter, BaseTarget, BasePromptValue
from ..converter import NoOpConverter


class SenderJob(BaseJob):
    def __init__(
        self,
        *,
        target: BaseTarget,
        converters: Sequence[BaseConverter] = [NoOpConverter()],
        include_original_prompt=False,
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)

        self._target = target
        self._converters = converters
        self._include_original_prompt = include_original_prompt

    def execute(
        self,
        *,
        run_id: Optional[str] = None,
        prompts: Sequence[Union[str, BasePromptValue]],
    ):
        if not run_id:
            run_id = self._create_run_id()

        for prompt in prompts:
            if isinstance(prompt, str):
                prompt = StringPromptValue(text=prompt)

            if self._include_original_prompt:
                self._target.send_prompt(prompt)

            for converter in self._converters:
                converted_prompt = converter.convert(prompt)
                response = self._target.send_prompt(converted_prompt)
                print(response)
