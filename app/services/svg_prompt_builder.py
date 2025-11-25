"""Prompt Builder for SVG Icon Generation."""


class SVGPromptBuilder:
    """Builds prompts for SVG icon generation."""

    SYSTEM_ROLE = """You are an expert SVG icon designer. You create clean, simple, scalable vector icons."""

    @staticmethod
    def build_svg_prompt(description: str) -> str:
        """Build a prompt that instructs the LLM to generate SVG code."""
        prompt = f"""{SVGPromptBuilder.SYSTEM_ROLE}

Generate a simple, clean SVG icon based on this description:
"{description}"

REQUIREMENTS:
- Output ONLY valid SVG code, nothing else
- Use viewBox="0 0 24 24" for consistency
- Keep the design minimal and clear
- Use solid colors (preferably black or single color)
- No gradients or complex effects
- Center the icon within the viewBox

IMPORTANT: Respond with ONLY the SVG code. Start with <svg and end with </svg>. No explanations, no markdown, no code blocks.

SVG:"""

        return prompt
