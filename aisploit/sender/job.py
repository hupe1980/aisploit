from typing import Union, Sequence, Optional, List
from datetime import datetime
from langchain_core.prompt_values import StringPromptValue

from ..core import (
    BaseJob,
    BaseConverter,
    BaseTarget,
    BasePromptValue,
    Callbacks,
    CallbackManager,
)
from ..converters import NoOpConverter
from .report import SendReport, SendReportEntry


class SenderJob(BaseJob):
    def __init__(
        self,
        *,
        target: BaseTarget,
        converters: List[BaseConverter] = [NoOpConverter()],
        include_original_prompt=False,
        callbacks: Callbacks = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)

        self._target = target
        self._converters = converters
        self._include_original_prompt = include_original_prompt
        self._callbacks = callbacks

    def execute(
        self,
        *,
        run_id: Optional[str] = None,
        prompts: Sequence[Union[str, BasePromptValue]],
    ) -> SendReport:
        run_id = run_id or self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self._callbacks,
        )

        report = SendReport(run_id=run_id)

        for prompt in prompts:
            if self._include_original_prompt and not any(
                isinstance(c, NoOpConverter) for c in self._converters
            ):
                self._converters.append(NoOpConverter())

            for converter in self._converters:
                if isinstance(prompt, str):
                    prompt = StringPromptValue(text=prompt)

                converted_prompt = converter.convert(prompt)

                entry = self._send_prompt(
                    prompt=converted_prompt,
                    converter=converter,
                    callback_manager=callback_manager,
                )

                report.add_entry(entry)

        return report

    def _send_prompt(
        self,
        *,
        prompt: BasePromptValue,
        converter: BaseConverter,
        callback_manager: CallbackManager,
    ) -> SendReportEntry:
        start_time = datetime.now()

        callback_manager.on_sender_send_prompt_start()

        response = self._target.send_prompt(prompt)

        callback_manager.on_sender_send_prompt_end()

        end_time = datetime.now()

        return SendReportEntry(
            prompt=prompt,
            converter=converter,
            response=response,
            start_time=start_time,
            end_time=end_time,
        )
