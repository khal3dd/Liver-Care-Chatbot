##Data Validation


from pydantic import BaseModel, Field, field_validator
from typing import Optional
from src.models.enums.ModelEnum import ModelEnum


class ChatRequest(BaseModel):
    message:    str             = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str]  = None
    model:      Optional[str]  = ModelEnum.default().value

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message cannot be blank.")
        return v.strip()


class ResetRequest(BaseModel):
    session_id: str


class CreateSessionRequest(BaseModel):
    model: Optional[str] = ModelEnum.default().value
