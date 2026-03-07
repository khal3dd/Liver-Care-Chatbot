
from __future__ import annotations
from src.models.ChatSession import ChatSession

class BaseController:
    """
    Central in-memory session registry.
    All controllers inherit from this to share the same store.

    Replace `_store` with a Redis or DB backend for production.
    """

    _store: dict[str, ChatSession] = {}

  
    def get_session(self, session_id: str) -> ChatSession | None:
        return self._store.get(session_id)

    def save_session(self, session: ChatSession) -> None:
        self._store[session.session_id] = session

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._store:
            del self._store[session_id]
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        return session_id in self._store

    def all_sessions(self) -> list[dict]:
        return [s.to_summary() for s in self._store.values()]

    def total_sessions(self) -> int:
        return len(self._store)
