from enum import Enum


class ModelEnum(str, Enum):
    """
    Supported OpenRouter models.
    Inherits from str so FastAPI serializes them directly.

    Usage:
        ModelEnum.GEMINI_FLASH.value  → "google/gemini-2.5-flash-lite"
        ModelEnum.GEMINI_FLASH.label  → "Gemini 2.5 Flash Lite"
        ModelEnum.GEMINI_FLASH.is_free → False
    """

    # ── Gemini ────────────────────────────────────────────
    GEMINI_FLASH      = "google/gemini-2.5-flash-lite"

    # ── Llama ─────────────────────────────────────────────
    LLAMA_3_1_8B      = "meta-llama/llama-3.1-8b-instruct:free"
    LLAMA_3_2_3B      = "meta-llama/llama-3.2-3b-instruct:free"

    # ── Mistral ───────────────────────────────────────────
    MISTRAL_7B        = "mistralai/mistral-7b-instruct:free"

    # ── Google ────────────────────────────────────────────
    GEMMA_2_9B        = "google/gemma-2-9b-it:free"

    # ── Microsoft ─────────────────────────────────────────
    PHI3_MINI         = "microsoft/phi-3-mini-128k-instruct:free"

    # ── Qwen ─────────────────────────────────────────────
    QWEN2_7B          = "qwen/qwen-2-7b-instruct:free"

    # ── Metadata ─────────────────────────────────────────
    _metadata = {
        "google/gemini-2.5-flash-lite":              ("Gemini 2.5 Flash Lite",  False),
        "meta-llama/llama-3.1-8b-instruct:free":     ("Llama 3.1 8B",           True),
        "meta-llama/llama-3.2-3b-instruct:free":     ("Llama 3.2 3B",           True),
        "mistralai/mistral-7b-instruct:free":         ("Mistral 7B",             True),
        "google/gemma-2-9b-it:free":                  ("Gemma 2 9B",             True),
        "microsoft/phi-3-mini-128k-instruct:free":    ("Phi-3 Mini 128K",        True),
        "qwen/qwen-2-7b-instruct:free":               ("Qwen2 7B",               True),
    }

    @property
    def label(self) -> str:
        return self._metadata.get(self.value, ("Unknown", False))[0]

    @property
    def is_free(self) -> bool:
        return self._metadata.get(self.value, ("Unknown", False))[1]

    @classmethod
    def values_list(cls) -> list[str]:
        """Return all model value strings."""
        return [m.value for m in cls if m.name != "_metadata"]

    @classmethod
    def default(cls) -> "ModelEnum":
        return cls.GEMINI_FLASH
