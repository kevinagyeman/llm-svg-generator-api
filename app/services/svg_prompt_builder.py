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

CRITICAL REQUIREMENTS:
- Output ONLY valid, well-formed SVG XML code
- ALL attribute values MUST be in double quotes (e.g., width="24" not width=24)
- Use viewBox="0 0 24 24" for consistency
- Include xmlns="http://www.w3.org/2000/svg" in the svg tag
- Keep the design minimal and clear
- Use solid colors (preferably black: fill="black" or stroke="black")
- No gradients or complex effects
- Center the icon within the viewBox
- Self-close empty tags (e.g., <path .../> not <path ...></path>)

STRICT FORMAT:
- Start IMMEDIATELY with <svg
- End with </svg>
- NO explanations before or after
- NO markdown code blocks
- NO text outside the SVG tags

Example valid format:
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="black"/></svg>

Now generate the SVG for: {description}"""

        return prompt
