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
    try:
        print(f"[DEBUG] Received chat request: message={req.message[:50]}, session_id={req.session_id}, model={req.model}")
        
        if not req.message.strip():
            return error(ResponseEnum.EMPTY_MESSAGE)

        result, status = chat_controller.handle_chat(
            message=req.message,
            session_id=req.session_id,
            model=req.model,
        )
        
        print(f"[DEBUG] Chat response: status={status.code}, message={status.message}")

        # Error statuses — return error shape
        if status not in (ResponseEnum.CHAT_SUCCESS, ResponseEnum.EMERGENCY):
            print(f"[DEBUG] Error status returned: {status.code}")
            return error(status)

        print(f"[DEBUG] Returning success response")
        return build_response(status, data=result)
        
    except Exception as e:
        print(f"[ERROR] Exception in chat route: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return error(ResponseEnum.UNKNOWN_ERROR)
