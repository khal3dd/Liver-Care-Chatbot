from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.models.enums.ModelEnum import ModelEnum


class Message(BaseModel):
    role:       str       # "user" | "assistant" | "system"
    content:    str
    timestamp:  datetime  = Field(default_factory=datetime.utcnow)


class ChatSession(BaseModel):
    session_id:     str
    model:          str           = ModelEnum.default().value
    history:        List[dict]    = Field(default_factory=list)
    message_count:  int           = 0
    created_at:     datetime      = Field(default_factory=datetime.utcnow)
    updated_at:     datetime      = Field(default_factory=datetime.utcnow)

    def add_turn(self, user_msg: str, assistant_msg: str) -> None:
        """Append a full user+assistant turn and update metadata."""
        self.history.append({"role": "user",      "content": user_msg})
        self.history.append({"role": "assistant",  "content": assistant_msg})
        self.message_count += 1
        self.updated_at = datetime.utcnow()

    def trim(self, max_turns: int) -> None:
        """Keep only the last max_turns messages."""
        if len(self.history) > max_turns:
            self.history = self.history[-max_turns:]

    def to_summary(self) -> dict:
        """Lightweight summary without full history."""
        return {
            "session_id":    self.session_id,
            "model":         self.model,
            "message_count": self.message_count,
            "created_at":    self.created_at.isoformat(),
            "updated_at":    self.updated_at.isoformat(),
        }
