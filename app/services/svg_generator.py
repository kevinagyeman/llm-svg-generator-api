"""SVG Icon Generator Service."""

import logging
import re
from typing import Optional, Tuple
from xml.etree import ElementTree as ET
from app.core.config import settings
from app.services.svg_prompt_builder import SVGPromptBuilder

logger = logging.getLogger(__name__)


class SVGGenerator:
    """Generates SVG icons using LLM."""

    def __init__(self):
        """Initialize the SVG generator."""
        self.prompt_builder = SVGPromptBuilder()

    def _get_client(
        self, provider: Optional[str] = None, api_key: Optional[str] = None
    ):
        """Get the appropriate LLM client based on provider."""
        provider = provider or settings.llm_provider

        if provider == "openai":
            from app.core.openai_client import openai_client

            return openai_client, "openai"
        elif provider == "anthropic":
            from app.core.anthropic_client import anthropic_client

            return anthropic_client, "anthropic"
        elif provider == "gemini":
            from app.core.gemini_client import gemini_client

            return gemini_client, "gemini"
        else:  # ollama
            from app.core.llm_client import ollama_client

            return ollama_client, "ollama"

    def generate_icon(
        self,
        description: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> Tuple[str, str, str]:
        """
        Generate an SVG icon based on a text description.

        Args:
            description: Text description of the desired icon
            provider: LLM provider to use ("openai", "gemini", "anthropic", "ollama")
            model: Specific model to use
            api_key: API key for the provider

        Returns:
            Tuple of (SVG code, provider used, model used)

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating SVG icon for: {description}")

            # Get the appropriate client
            client, provider_used = self._get_client(provider, api_key)
            logger.info(f"Using provider: {provider_used}")

            # Build the prompt
            prompt = self.prompt_builder.build_svg_prompt(description)

            # Prepare generation parameters
            gen_params = {
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 1000,
            }

            # Add api_key if provided
            if api_key:
                gen_params["api_key"] = api_key

            # Add model if provided
            if model:
                gen_params["model"] = model

            # Call LLM
            llm_response = client.generate(**gen_params)

            response_text = llm_response["response"]
            model_used = llm_response.get("model", model or "unknown")

            logger.debug(f"LLM response length: {len(response_text)}")
            logger.debug(f"Raw LLM response: {response_text[:500]}...")

            # Extract SVG code
            svg_code = self._extract_svg(response_text)

            if not svg_code:
                logger.warning("No valid SVG found in response")
                logger.warning(f"Full response was: {response_text}")
                return self._fallback_svg(description), provider_used, model_used

            # Validate SVG
            if not self._validate_svg(svg_code):
                logger.warning("SVG validation failed, using fallback")
                logger.warning(f"Invalid SVG: {svg_code}")
                return self._fallback_svg(description), provider_used, model_used

            logger.info("SVG icon generated successfully")
            return svg_code, provider_used, model_used

        except Exception as e:
            logger.error(f"SVG generation error: {str(e)}", exc_info=True)
            # Re-raise the exception so it can be handled by the route
            raise

    def _extract_svg(self, text: str) -> Optional[str]:
        """Extract SVG code from LLM response."""
        # Remove markdown code blocks if present
        text = re.sub(r"```svg\n?", "", text)
        text = re.sub(r"```xml\n?", "", text)
        text = re.sub(r"```\n?", "", text)

        # Remove any leading/trailing text
        text = text.strip()

        # Try to find SVG tags (case-insensitive, multiline)
        svg_match = re.search(r"<svg[^>]*>.*?</svg>", text, re.DOTALL | re.IGNORECASE)

        if svg_match:
            svg_code = svg_match.group(0)
            # Clean up the SVG
            svg_code = self._clean_svg(svg_code)
            return svg_code.strip()

        return None

    def _clean_svg(self, svg_code: str) -> str:
        """Clean and normalize SVG code."""
        svg_code = svg_code.replace('\\"', '"')
        svg_code = svg_code.replace("\\'", "'")
        svg_code = svg_code.replace("\\n", "")
        svg_code = svg_code.replace("\\t", "")
        svg_code = re.sub(r"\s+", " ", svg_code)
        svg_code = re.sub(r">\s+<", "><", svg_code)
        return svg_code.strip()

    def _validate_svg(self, svg_code: str) -> bool:
        """Validate that SVG code is well-formed XML."""
        try:
            # Try to parse as XML
            ET.fromstring(svg_code)
            return True
        except ET.ParseError as e:
            logger.error(f"SVG XML parsing error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"SVG validation error: {str(e)}")
            return False

    def _fallback_svg(self, description: str) -> str:
        """Return a simple fallback SVG if generation fails."""
        return """SVG icon fallback"""


# Create singleton instance
svg_generator = SVGGenerator()
