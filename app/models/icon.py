"""SVG icon generation data models."""

from typing import Literal
from pydantic import BaseModel, Field


class IconGenerationRequest(BaseModel):
    """SVG icon generation request."""

    prompt: str = Field(..., description="Icon description", examples=["a rocket ship"])
    provider: Literal["openai", "gemini", "anthropic", "ollama"] = Field(
        ..., description="LLM provider", examples=["openai"]
    )
    model: str = Field(..., description="Model name", examples=["gpt-4"])


class IconGenerationResponse(BaseModel):
    """SVG icon generation response."""

    icon: str = Field(..., description="Generated SVG code")
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
