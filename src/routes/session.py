from fastapi import APIRouter
from src.schemas.chat import ResetRequest, CreateSessionRequest
from src.controllers.SessionController import session_controller
from src.helpers.response_helper import build_response, error
from src.models.enums.ResponseEnum import ResponseEnum

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.post("")
def create_session(req: CreateSessionRequest):
    """Explicitly create a new session."""
    data, status = session_controller.create_session(model=req.model)
    return build_response(status, data=data)


@router.get("")
def list_sessions():
    """List all active sessions (summary only)."""
    data, status = session_controller.list_sessions()
    return build_response(status, data=data)


@router.get("/{session_id}")
def get_session(session_id: str):
    """Get full session info including history."""
    data, status = session_controller.get_session_info(session_id)
    if data is None:
        return error(ResponseEnum.SESSION_404)
    return build_response(status, data=data)


@router.delete("/{session_id}")
def reset_session(session_id: str):
    """Delete a session and its history."""
    data, status = session_controller.reset_session(session_id)
    if status == ResponseEnum.SESSION_404:
        return error(ResponseEnum.SESSION_404)
    return build_response(status, data=data)
