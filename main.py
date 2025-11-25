"""
LLM SVG Generator API - Main Application

Entry point for the SVG icon generation service.
Run: uvicorn main:app --reload --port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="LLM SVG Generator API",
    description="""
    AI-powered SVG icon generation API.

    Generate custom SVG icons from text descriptions using Large Language Models.
    Perfect for creating scalable vector graphics on-demand.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# WARNING: allow_origins=["*"] is for development only
# In production, specify exact domains to prevent CSRF attacks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint - provides API information."""
    return {
        "message": "LLM SVG Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "generate_endpoint": "/api/v1/generate",
    }
