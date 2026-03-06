import uuid
from src.controllers.BaseController import BaseController
from src.services.llm_service import llm_service
from src.models.ChatSession import ChatSession
from src.models.enums.ResponseEnum import ResponseEnum
from src.models.enums.ModelEnum import ModelEnum
from src.config.settings import settings


class ChatController(BaseController):

    def handle_chat(
        self,
        message: str,
        session_id: str | None,
        model: str | None,
    ) -> tuple[dict, ResponseEnum]:
        """
        Full chat turn pipeline:
          1. Resolve or create session
          2. Call LLM service
          3. Persist updated session
          4. Return (result_dict, status)
        """
        # Resolve session
        session_id = session_id or str(uuid.uuid4())
        session    = self.get_session(session_id)

        if session is None:
            session = ChatSession(
                session_id=session_id,
                model=model or settings.DEFAULT_MODEL,
            )

        # Validate model
        valid_models = ModelEnum.values_list()
        chosen_model = model or session.model
        if chosen_model not in valid_models:
            chosen_model = settings.DEFAULT_MODEL

        # Call service
        reply, updated_history, status = llm_service.chat(
            user_message=message,
            history=session.history,
            model=chosen_model,
        )

        # Persist only on success or emergency
        if status in (ResponseEnum.CHAT_SUCCESS, ResponseEnum.EMERGENCY):
            session.history = updated_history
            session.message_count += 1
            self.save_session(session)

        result = {
            "reply":          reply,
            "session_id":     session_id,
            "is_emergency":   status == ResponseEnum.EMERGENCY,
            "history_length": len(updated_history),
            "model":          chosen_model,
        }
        return result, status


# Singleton
chat_controller = ChatController()
