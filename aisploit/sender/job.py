from typing import Union, Sequence, Optional
from datetime import datetime
from langchain_core.prompt_values import StringPromptValue

from ..core import BaseJob, BaseConverter, BaseTarget, BasePromptValue
from ..converter import NoOpConverter
from .report import SendReport, SendReportEntry


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
    ) -> SendReport:
        run_id = run_id or self._create_run_id()

        report = SendReport(run_id=run_id)

        for prompt in prompts:
            if isinstance(prompt, str):
                prompt = StringPromptValue(text=prompt)

            if self._include_original_prompt and not any(
                isinstance(c, NoOpConverter) for c in self._converters
            ):
                entry = self._send_prompt(prompt)
                report.add_entry(entry)

            for converter in self._converters:
                converted_prompt = converter.convert(prompt)
                entry = self._send_prompt(converted_prompt, converter)
                report.add_entry(entry)

        return report

    def _send_prompt(
        self, prompt: BasePromptValue, converter: Optional[BaseConverter] = None
    ) -> SendReportEntry:
        start_time = datetime.now()
        response = self._target.send_prompt(prompt).strip()
        end_time = datetime.now()

        return SendReportEntry(
            prompt=prompt,
            converter=converter,
            response=response,
            start_time=start_time,
            end_time=end_time,
        )
