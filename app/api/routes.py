"""
API route handlers for SVG icon generation endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Query
from app.models.icon import IconGenerationRequest, IconGenerationResponse
from datetime import datetime
import logging
from app.services.svg_generator import svg_generator

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["svg-generation"],
)


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
) -> IconGenerationResponse:
    """
    Generate an SVG icon from a text description.

    The LLM will create a simple, clean SVG icon matching your description.
    Icons are generated with viewBox="0 0 24 24" for consistency.

    Args:
        request: Icon generation request containing the prompt

    Returns:
        IconGenerationResponse with the generated SVG code

    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Generating SVG icon for prompt: {request.prompt}")

        # Generate SVG icon using the service
        svg_code = svg_generator.generate_icon(request.prompt)

        response = IconGenerationResponse(icon=svg_code)

        logger.info(f"SVG icon generated successfully")

        return response

    except Exception as e:
        logger.error(
            f"Error generating SVG icon: {str(e)}",
            exc_info=True,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the SVG icon: {str(e)}",
        )
