from typing import Optional
from langchain_core.prompt_values import StringPromptValue
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
    GetSessionHistoryCallable,
)

from ..core import (
    BaseChatModel,
    BaseClassifier,
    BaseJob,
    BaseTarget,
    Callbacks,
    CallbackManager,
)
from .task import RedTeamTask
from .report import RedTeamReport, RedTeamReportEntry


class RedTeamJob(BaseJob):
    def __init__(
        self,
        *,
        chat_model: BaseChatModel,
        task: RedTeamTask,
        target: BaseTarget,
        classifier: BaseClassifier,
        get_session_history: Optional[GetSessionHistoryCallable] = None,
        callbacks: Callbacks = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)

        self._chat_model = chat_model
        self._task = task
        self._target = target
        self._classifier = classifier
        self._get_session_history = (
            get_session_history
            if get_session_history
            else lambda *args, **kwargs: ChatMessageHistory()
        )
        self._callbacks = callbacks

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
            callbacks=self._callbacks,
        )

        runnable = self._task.prompt | self._chat_model | StrOutputParser()

        chain = RunnableWithMessageHistory(
            runnable,  # type: ignore[arg-type]
            get_session_history=self._get_session_history,
            input_messages_key=self._task.input_messages_key,
            history_messages_key=self._task.history_messages_key,
        )

        report = RedTeamReport(run_id=run_id)

        current_prompt_text = initial_prompt_text

        for attempt in range(1, max_attempt + 1):
            current_prompt_text = chain.invoke(
                input={self._task.input_messages_key: current_prompt_text},
                config={"configurable": {"session_id": run_id}},
            )

            current_prompt = StringPromptValue(text=current_prompt_text)

            callback_manager.on_redteam_attempt_start(attempt, current_prompt)

            response = self._target.send_prompt(current_prompt)

            score = self._classifier.score_text(text=response)

            callback_manager.on_redteam_attempt_end(attempt, response, score)

            report.add_entry(
                RedTeamReportEntry(
                    attempt=attempt,
                    prompt=current_prompt,
                    response=response,
                    score=score,
                )
            )

            if score.flagged:
                break

            current_prompt_text = response

        return report
