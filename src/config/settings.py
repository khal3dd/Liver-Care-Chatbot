
#env/system validation and configuration management using pydantic

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):

    # ── App ───────────────────────────────────────────────
    APP_TITLE:   str = "Kidney Care Chatbot"
    APP_VERSION: str = "2.0.0"

    # ── OpenRouter ────────────────────────────────────────
    OPENROUTER_API_KEY:  str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL:       str = "google/gemini-2.5-flash-lite"
    MAX_TOKENS:          int = 700
    TEMPERATURE:       float = 0.4
    MAX_HISTORY_TURNS:   int = 20

    # ── Server ────────────────────────────────────────────
    APP_HOST: str  = "0.0.0.0"
    APP_PORT: int  = 8000
    DEBUG:    bool = False

    # ── CORS ──────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["*"]

    # ── OpenRouter extra headers ──────────────────────────
    @property
    def EXTRA_HEADERS(self) -> dict:
        return {
            "HTTP-Referer": "https://kidney-care-chatbot.app",
            "X-Title": self.APP_TITLE,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
