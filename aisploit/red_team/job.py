from dataclasses import dataclass, field
from typing import Optional

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.runnables.history import (
    GetSessionHistoryCallable,
    RunnableWithMessageHistory,
)
from tqdm.auto import tqdm

from .report import RedTeamReport, RedTeamReportEntry
from .task import RedTeamTask
from ..core import (
    BaseChatModel,
    BaseConverter,
    BaseJob,
    BaseTarget,
    CallbackManager,
    Callbacks,
)

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


@dataclass
class RedTeamJob(BaseJob):
    chat_model: BaseChatModel
    task: RedTeamTask
    target: BaseTarget
    get_session_history: GetSessionHistoryCallable = get_session_history
    converter: Optional[BaseConverter] = None
    callbacks: Callbacks = field(default_factory=list)

    def execute(
        self,
        *,
        run_id: Optional[str] = None,
        initial_prompt_text="Begin Conversation",
        max_attempt=5,
    ) -> RedTeamReport:
        run_id = run_id or self._create_run_id()

        callback_manager = CallbackManager(
            run_id=run_id,
            callbacks=self.callbacks,
        )

        runnable = self.task.prompt | self.chat_model | StrOutputParser()

        chain = RunnableWithMessageHistory(
            runnable,  # type: ignore[arg-type]
            get_session_history=self.get_session_history,
            input_messages_key=self.task.input_messages_key,
            history_messages_key=self.task.history_messages_key,
        )

        report = RedTeamReport(run_id=run_id)

        current_prompt_text = initial_prompt_text

        for attempt in tqdm(range(1, max_attempt + 1), desc="Attacking", disable=self.disable_progressbar):
            current_prompt_text = chain.invoke(
                input={self.task.input_messages_key: current_prompt_text},
                config={"configurable": {"session_id": run_id}},
            )

            current_prompt = (
                self.converter.convert(current_prompt_text)
                if self.converter
                else StringPromptValue(text=current_prompt_text)
            )

            callback_manager.on_redteam_attempt_start(attempt, current_prompt)

            response = self.target.send_prompt(current_prompt)

            score = self.task.evaluate_task_completion(response, get_session_history(session_id=run_id))

            callback_manager.on_redteam_attempt_end(attempt, response, score)

            report.add_entry(
                RedTeamReportEntry(
                    attempt=attempt,
                    prompt=current_prompt,
                    response=response,
                    score=score,
                )
            )

            if score.flagged:  # task is completed
                break

            current_prompt_text = response.content

        return report
