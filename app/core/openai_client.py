"""OpenAI API client."""

from openai import OpenAI
from typing import Dict, Any
from app.core.config import settings


class OpenAIClient:
    """OpenAI API client."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model_name = model or "gpt-4"
        self.client = OpenAI(api_key=api_key) if api_key else None

    def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        api_key: str = None,
        model: str = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate completion from OpenAI."""
        temperature = (
            temperature if temperature is not None else settings.llm_temperature
        )
        max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens
        current_api_key = api_key or self.api_key
        current_model = model or self.model_name

        if not current_api_key:
            raise ValueError("OpenAI API key required")

        client = OpenAI(api_key=current_api_key)

        try:
            response = client.chat.completions.create(
                model=current_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return {
                "response": response.choices[0].message.content,
                "model": current_model,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


openai_client = OpenAIClient()
