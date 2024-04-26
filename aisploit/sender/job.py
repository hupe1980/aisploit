from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union

from tqdm.auto import tqdm

from .report import SendReport, SendReportEntry
from ..converters import NoOpConverter
from ..core import (
    BaseConverter,
    BaseJob,
    BasePromptValue,
    BaseTarget,
    CallbackManager,
    Callbacks,
    Prompt,
    StringPromptValue,
)


@dataclass
class SenderJob(BaseJob):
    target: BaseTarget
    converters: List[BaseConverter] = field(default_factory=lambda: [NoOpConverter()])
    include_original_prompt: bool = False
    callbacks: Callbacks = field(default_factory=list)

    def execute(
        self,
        *,
        run_id: Optional[str] = None,
        prompts: Sequence[Union[str, Prompt]],
    ) -> SendReport:
        run_id = run_id or self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self.callbacks,
        )

        report = SendReport(run_id=run_id)

        for prompt in tqdm(prompts, desc="Sending", disable=self.disable_progressbar):
            if self.include_original_prompt and not any(isinstance(c, NoOpConverter) for c in self.converters):
                self.converters.append(NoOpConverter())

            for converter in self.converters:
                if isinstance(prompt, str):
                    prompt = Prompt(value=StringPromptValue(text=prompt))

                converted_prompt_value = converter.convert(prompt.value)

                entry = self._send(
                    prompt_value=converted_prompt_value,
                    converter=converter,
                    metadata=prompt.metadata,
                    callback_manager=callback_manager,
                )

                report.add_entry(entry)

        return report

    def _send(
        self,
        *,
        prompt_value: BasePromptValue,
        converter: BaseConverter,
        metadata: Dict[str, Any],
        callback_manager: CallbackManager,
    ) -> SendReportEntry:
        start_time = datetime.now()

        callback_manager.on_sender_send_prompt_start()

        response = self.target.send_prompt(prompt_value)

        callback_manager.on_sender_send_prompt_end()

        end_time = datetime.now()

        return SendReportEntry(
            prompt_value=prompt_value,
            metadata=metadata,
            converter=converter,
            response=response,
            start_time=start_time,
            end_time=end_time,
        )
