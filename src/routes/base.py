from fastapi import APIRouter
from src.config.settings import settings
from src.models.enums.ModelEnum import ModelEnum
from src.helpers.response_helper import build_response, success
from src.models.enums.ResponseEnum import ResponseEnum

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return build_response(
        ResponseEnum.SUCCESS,
        data={"status": "ok"},
    )


@router.get("/info")
def info():
    return success(data={
        "app":           settings.APP_TITLE,
        "version":       settings.APP_VERSION,
        "default_model": settings.DEFAULT_MODEL,
        "status":        "running",
    })


@router.get("/models")
def list_models():
    """Return all available LLM models."""
    return success(data={
        "models": ModelEnum.values_list(),
        "default": ModelEnum.default().value,
    })
