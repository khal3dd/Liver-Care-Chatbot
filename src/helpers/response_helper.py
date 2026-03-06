from fastapi.responses import JSONResponse
from src.models.enums.ResponseEnum import ResponseEnum


def build_response(
    status: ResponseEnum,
    data: dict = None,
    message_override: str = None,
) -> JSONResponse:
    """
    Build a standardized JSON response.

    Every API response follows this shape:
    {
        "code":    10,
        "message": "Chat response generated",
        "data":    { ... }
    }

    Args:
        status           : ResponseEnum member
        data             : payload dict (optional)
        message_override : custom message (optional, overrides enum message)
    """
    return JSONResponse(
        status_code=status.http_status,
        content={
            "code":    status.code,
            "message": message_override or status.message,
            "data":    data or {},
        },
    )


def success(data: dict = None, message: str = None) -> JSONResponse:
    return build_response(ResponseEnum.SUCCESS, data, message)


def error(status: ResponseEnum, message: str = None) -> JSONResponse:
    return build_response(status, message_override=message)
