from typing import List

from .bot import RedTeamingBot
from ..core import BaseJob, BaseTarget, BaseCallbackHandler, CallbackManager
from ..classifier import BaseClassifier

class RedTeamJob(BaseJob):
    def __init__(
        self, 
        *,
        bot: RedTeamingBot,
        target: BaseTarget,
        classifier: BaseClassifier,
        initial_prompt: str = "Begin Conversation",
        callbacks: List[BaseCallbackHandler] = [],
        verbose=False,
    ) -> None:
        super().__init__(verbose=verbose)
        
        self._bot = bot
        self._target = target
        self._classifier = classifier
        self._initial_prompt = initial_prompt
        self._callback_manager = CallbackManager(
            id=self.conversation_id,
            callbacks=callbacks,
        )

    @property
    def conversation_id(self):
        return self._bot.conversation_id
    
    def execute(self, max_attempt=5, clear_history=True):
        if clear_history:
            self._bot.clear_history()

        current_prompt = self._initial_prompt
        
        for attempt in range(1, max_attempt+1):
            current_prompt = self._bot.invoke(current_prompt)
            
            self._callback_manager.on_redteam_attempt(attempt, current_prompt)
            
            response = self._target.send_prompt(current_prompt)
            score = self._classifier.score_text(text=response)

            self._callback_manager.on_redteam_attempt_response(attempt, response)
            
            if score.score_value:
                return score

    