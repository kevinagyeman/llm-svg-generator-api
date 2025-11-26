"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    api_title: str = "LLM SVG Generator API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered SVG icon generation API"
    debug: bool = True

    llm_provider: str = "gemini"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    llm_top_p: float = 0.9

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout: int = 30

    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
