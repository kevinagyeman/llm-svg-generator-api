"""LLM SVG Generator API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="LLM SVG Generator API",
    description="AI-powered SVG icon generation using multiple LLM providers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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
    """API information."""
    return {
        "message": "LLM SVG Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "generate_endpoint": "/api/v1/generate",
    }
