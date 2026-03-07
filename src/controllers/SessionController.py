import uuid
from src.controllers.BaseController import BaseController
from src.models.ChatSession import ChatSession
from src.models.enums.ResponseEnum import ResponseEnum
from src.config.settings import settings


class SessionController(BaseController):

    def create_session(self, model: str = None) -> tuple[dict, ResponseEnum]:
        session = ChatSession(
            session_id=str(uuid.uuid4()),
            model=model or settings.DEFAULT_MODEL,
        )
        self.save_session(session)
        return session.to_summary(), ResponseEnum.SESSION_CREATED

    def get_session_info(self, session_id: str) -> tuple[dict | None, ResponseEnum]:
        session = self.get_session(session_id)
        if session is None:
            return None, ResponseEnum.SESSION_404
        return {
            **session.to_summary(),
            "history": session.history,
        }, ResponseEnum.SESSION_FOUND

    def reset_session(self, session_id: str) -> tuple[dict, ResponseEnum]:
        deleted = self.delete_session(session_id)
        if not deleted:
            return {}, ResponseEnum.SESSION_404
        return {"session_id": session_id}, ResponseEnum.SESSION_RESET

    def list_sessions(self) -> tuple[dict, ResponseEnum]:
        return {
            "total":    self.total_sessions(),
            "sessions": self.all_sessions(),
        }, ResponseEnum.SUCCESS


session_controller = SessionController()
