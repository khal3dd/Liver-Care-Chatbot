from enum import Enum


class ResponseEnum(Enum):
    """
    Each entry is a tuple of (code, message, http_status).

    Usage:
        ResponseEnum.SUCCESS.value        → (1, "Success", 200)
        ResponseEnum.SUCCESS.code         → 1
        ResponseEnum.SUCCESS.message      → "Success"
        ResponseEnum.SUCCESS.http_status  → 200
    """

  
    SUCCESS       = (1,  "Success",                        200)
    UNKNOWN_ERROR = (2,  "An unexpected error occurred",   500)


    CHAT_SUCCESS  = (10, "Chat response generated",        200)
    CHAT_ERROR    = (11, "Chat processing failed",         502)
    EMERGENCY     = (12, "Emergency detected",             200)
    EMPTY_MESSAGE = (13, "Message cannot be empty",        422)

    SESSION_CREATED = (20, "Session created",              201)
    SESSION_FOUND   = (21, "Session found",                200)
    SESSION_RESET   = (22, "Session reset successfully",   200)
    SESSION_404     = (23, "Session not found",            404)

    INVALID_API_KEY = (30, "Invalid or missing API key",   401)
    MODEL_BUSY      = (31, "Model is busy, try another",   429)
    MODEL_ERROR     = (32, "Model returned no response",   502)
    
    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]

    @property
    def http_status(self) -> int:
        return self.value[2]
