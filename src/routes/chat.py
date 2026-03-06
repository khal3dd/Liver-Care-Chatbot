from fastapi import APIRouter
from src.schemas.chat import ChatRequest
from src.controllers.ChatController import chat_controller
from src.helpers.response_helper import build_response, error
from src.models.enums.ResponseEnum import ResponseEnum

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat")
def chat(req: ChatRequest):
    """
    Send a message and receive an AI response.
    Creates a new session automatically if session_id is not provided.
    """
    if not req.message.strip():
        return error(ResponseEnum.EMPTY_MESSAGE)

    result, status = chat_controller.handle_chat(
        message=req.message,
        session_id=req.session_id,
        model=req.model,
    )

    # Error statuses — return error shape
    if status not in (ResponseEnum.CHAT_SUCCESS, ResponseEnum.EMERGENCY):
        return error(status)

    return build_response(status, data=result)
