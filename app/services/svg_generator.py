"""SVG Icon Generator Service."""

import logging
import re
from typing import Optional
from app.core.llm_client import ollama_client
from app.services.svg_prompt_builder import SVGPromptBuilder

logger = logging.getLogger(__name__)


class SVGGenerator:
    """Generates SVG icons using LLM."""

    def __init__(self):
        """Initialize the SVG generator."""
        self.client = ollama_client
        self.prompt_builder = SVGPromptBuilder()

    def generate_icon(self, description: str) -> str:
        """
        Generate an SVG icon based on a text description.

        Args:
            description: Text description of the desired icon

        Returns:
            SVG code as a string

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating SVG icon for: {description}")

            # Build the prompt
            prompt = self.prompt_builder.build_svg_prompt(description)

            # Call LLM with higher temperature for creativity
            llm_response = self.client.generate(
                prompt=prompt,
                temperature=0.7,  # More creative
                max_tokens=1000,  # Enough for SVG code
            )

            response_text = llm_response["response"]
            logger.debug(f"LLM response length: {len(response_text)}")

            # Extract SVG code
            svg_code = self._extract_svg(response_text)

            if not svg_code:
                logger.warning("No valid SVG found in response")
                return self._fallback_svg(description)

            logger.info("SVG icon generated successfully")
            return svg_code

        except Exception as e:
            logger.error(f"SVG generation error: {str(e)}", exc_info=True)
            return self._fallback_svg(description)

    def _extract_svg(self, text: str) -> Optional[str]:
        """Extract SVG code from LLM response."""
        # Remove markdown code blocks if present
        text = re.sub(r"```svg\n?", "", text)
        text = re.sub(r"```\n?", "", text)

        # Find SVG tags
        svg_match = re.search(r"<svg[^>]*>.*?</svg>", text, re.DOTALL | re.IGNORECASE)

        if svg_match:
            svg_code = svg_match.group(0)
            # Basic validation
            if "<svg" in svg_code.lower() and "</svg>" in svg_code.lower():
                return svg_code.strip()

        return None

    def _fallback_svg(self, description: str) -> str:
        """Return a simple fallback SVG if generation fails."""
        return f"""<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="none" stroke="black" stroke-width="2"/>
  <text x="12" y="16" text-anchor="middle" font-size="10" fill="black">?</text>
</svg>"""


# Create singleton instance
svg_generator = SVGGenerator()
