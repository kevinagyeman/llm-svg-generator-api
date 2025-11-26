"""Anthropic API client."""

from anthropic import Anthropic
from typing import Dict, Any
from app.core.config import settings


class AnthropicClient:
    """Anthropic Claude API client."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model_name = model or "claude-3-5-sonnet-20241022"
        self.client = Anthropic(api_key=api_key) if api_key else None

    def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        api_key: str = None,
        model: str = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate completion from Anthropic."""
        temperature = (
            temperature if temperature is not None else settings.llm_temperature
        )
        max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens
        current_api_key = api_key or self.api_key
        current_model = model or self.model_name

        if not current_api_key:
            raise ValueError("Anthropic API key required")

        client = Anthropic(api_key=current_api_key)

        try:
            response = client.messages.create(
                model=current_model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )

            return {
                "response": response.content[0].text,
                "model": current_model,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")


anthropic_client = AnthropicClient()
