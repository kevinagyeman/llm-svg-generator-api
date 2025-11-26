"""Google Gemini API client."""

import google.generativeai as genai
from typing import Dict, Any
from app.core.config import settings


class GeminiClient:
    """Google Gemini API client."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model or settings.gemini_model

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        api_key: str = None,
        model: str = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate completion from Gemini."""
        temperature = (
            temperature if temperature is not None else settings.llm_temperature
        )
        max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens
        current_api_key = api_key or self.api_key
        current_model = model or self.model_name

        if not current_api_key:
            raise ValueError("Gemini API key required")

        genai.configure(api_key=current_api_key)
        model_instance = genai.GenerativeModel(current_model)

        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=settings.llm_top_p,
        )

        try:
            response = model_instance.generate_content(
                prompt, generation_config=generation_config
            )

            return {
                "response": response.text,
                "model": current_model,
                "finish_reason": response.candidates[0].finish_reason.name
                if response.candidates
                else None,
            }
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")


gemini_client = GeminiClient()
