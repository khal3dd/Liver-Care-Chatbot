from openai import OpenAI, AuthenticationError, RateLimitError
from src.config.settings import settings
from src.config.prompts import SYSTEM_PROMPT, EMERGENCY_KEYWORDS, EMERGENCY_RESPONSE
from src.models.enums.ResponseEnum import ResponseEnum


class LLMService:


    def _get_client(self) -> OpenAI:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError(ResponseEnum.INVALID_API_KEY.message)
        return OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )

    
    def is_emergency(self, text: str) -> bool:
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in EMERGENCY_KEYWORDS)

   
    def trim_history(self, history: list) -> list:
        if len(history) > settings.MAX_HISTORY_TURNS:
            return history[-settings.MAX_HISTORY_TURNS:]
        return history

    def build_messages(self, history: list) -> list:
        return [{"role": "system", "content": SYSTEM_PROMPT}] + history

   
    def chat(
        self,
        user_message: str,
        history: list,
        model: str = None,
    ) -> tuple[str, list, ResponseEnum]:
        """
        Send a message and return (reply, updated_history, status).

        Returns:
            reply          : assistant response text
            updated_history: history including this turn
            status         : ResponseEnum (CHAT_SUCCESS | EMERGENCY | error code)
        """
        model = model or settings.DEFAULT_MODEL

       
        if self.is_emergency(user_message):
            return EMERGENCY_RESPONSE, history, ResponseEnum.EMERGENCY

        history = self.trim_history(
            history + [{"role": "user", "content": user_message}]
        )

        try:
            client   = self._get_client()
            messages = self.build_messages(history)

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                stream=False,
                extra_headers=settings.EXTRA_HEADERS,
            )

            reply = response.choices[0].message.content or ""

            if not reply:
                return "", history, ResponseEnum.MODEL_ERROR

            updated_history = self.trim_history(
                history + [{"role": "assistant", "content": reply}]
            )
            return reply, updated_history, ResponseEnum.CHAT_SUCCESS

        except AuthenticationError:
            return "", history, ResponseEnum.INVALID_API_KEY

        except RateLimitError:
            return "", history, ResponseEnum.MODEL_BUSY

        except Exception as e:
            return str(e), history, ResponseEnum.CHAT_ERROR


llm_service = LLMService()