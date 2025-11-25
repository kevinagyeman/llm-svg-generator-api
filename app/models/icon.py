"""
SVG Icon Generation data models using Pydantic.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class IconGenerationRequest(BaseModel):
    """Input model for SVG icon generation requests."""

    prompt: str = Field(
        ...,
        description="Description of the icon to generate",
        examples=["a simple rocket ship"],
    )


class IconGenerationResponse(BaseModel):
    """Output model for SVG icon generation results."""

    icon: str = Field(..., description="Generated SVG code")
