"""SVG icon generation API routes."""

from fastapi import APIRouter, HTTPException, status, Header
from app.models.icon import IconGenerationRequest, IconGenerationResponse
import logging
from typing import Optional
from app.services.svg_generator import svg_generator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["svg-generation"])


@router.post(
    "/generate",
    response_model=IconGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate SVG icon from text description",
    description="""
    Generates a custom SVG icon based on a text description using AI.

    The endpoint:
    1. Validates the incoming request
    2. Builds an optimized prompt for SVG generation
    3. Calls the LLM to generate SVG code
    4. Extracts and validates the SVG output
    5. Returns clean, minimal SVG code

    **Use this endpoint when**:
    - You need custom icons for your application
    - You want AI-generated vector graphics
    - You need scalable icons based on descriptions
    """,
)
async def generate(
    request: IconGenerationRequest,
    x_api_key: Optional[str] = Header(None),
) -> IconGenerationResponse:
    """Generate SVG icon from text description using specified LLM provider."""
    try:
        logger.info(
            f"Generating SVG: {request.prompt} ({request.provider}/{request.model})"
        )

        if not x_api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required. Pass it in X-API-Key header.",
            )

        svg_code, provider_used, model_used = svg_generator.generate_icon(
            description=request.prompt,
            provider=request.provider,
            model=request.model,
            api_key=x_api_key,
        )

        logger.info(f"SVG generated successfully: {provider_used}/{model_used}")

        return IconGenerationResponse(
            icon=svg_code,
            provider=provider_used,
            model=model_used,
        )

    except HTTPException:
        raise
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)

        logger.error(
            f"SVG generation failed: {error_type}: {error_message}", exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": error_type, "message": error_message},
        )
