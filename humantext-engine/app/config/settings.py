"""
HumanText Engine — Configuration & Settings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All configuration is loaded from environment variables via pydantic-settings.
ZERO hardcoded credentials. All secrets come from .env file.

Usage:
    from app.config.settings import get_settings
    settings = get_settings()
    print(settings.PRIMARY_MODEL)
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    """Supported log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(str, Enum):
    """Supported log formats."""
    JSON = "json"
    CONSOLE = "console"


class Settings(BaseSettings):
    """
    Centralized settings for the HumanText Engine.
    
    All values are loaded from environment variables.
    Defaults are safe for development; production overrides via .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── LLM Provider API Keys ──────────────────────────────────────
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")
    GOOGLE_API_KEY: str = Field(default="", description="Google AI API key")

    # ── Observability ──────────────────────────────────────────────
    LANGSMITH_API_KEY: str = Field(default="", description="LangSmith API key for tracing")
    LANGSMITH_PROJECT: str = Field(default="humantext-engine", description="LangSmith project name")
    LANGSMITH_TRACING: bool = Field(default=False, description="Enable LangSmith tracing")

    # ── Model Configuration ────────────────────────────────────────
    PRIMARY_MODEL: str = Field(default="gpt-4o", description="Primary LLM for complex tasks")
    ANALYSIS_MODEL: str = Field(default="gpt-4o-mini", description="Lighter model for analysis")
    VALIDATION_MODEL: str = Field(default="gpt-4o-mini", description="Model for validation checks")
    REWRITE_MODEL: str = Field(default="gpt-4o", description="Model for text rewriting")
    REVISION_MODEL: str = Field(default="gpt-4o", description="Model for revision passes")
    EMBEDDING_MODEL: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence-transformers model for embeddings",
    )

    # ── Quality Thresholds ─────────────────────────────────────────
    SEMANTIC_THRESHOLD: float = Field(
        default=0.85, ge=0.0, le=1.0,
        description="Minimum semantic similarity score to pass (Dimension 12 hard gate)",
    )
    FACT_THRESHOLD: float = Field(
        default=0.95, ge=0.0, le=1.0,
        description="Minimum factual consistency score to pass",
    )
    STYLE_THRESHOLD: float = Field(
        default=0.70, ge=0.0, le=1.0,
        description="Minimum style conformance score",
    )
    NATURALNESS_THRESHOLD: float = Field(
        default=0.70, ge=0.0, le=1.0,
        description="Minimum naturalness score",
    )
    QUALITY_THRESHOLD: float = Field(
        default=0.75, ge=0.0, le=1.0,
        description="Minimum composite quality score to pass",
    )

    # ── Limits ─────────────────────────────────────────────────────
    MAX_REVISIONS: int = Field(
        default=3, ge=1, le=10,
        description="Maximum revision loops before returning best-effort output",
    )
    MAX_INPUT_LENGTH: int = Field(
        default=50000, ge=100,
        description="Maximum input text length in characters",
    )
    MAX_OUTPUT_TOKENS: int = Field(
        default=8192, ge=256,
        description="Maximum output tokens per LLM call",
    )
    REQUEST_TIMEOUT: int = Field(
        default=120, ge=10,
        description="Maximum seconds for a single request",
    )

    # ── Server ─────────────────────────────────────────────────────
    HOST: str = Field(default="0.0.0.0", description="Server bind host")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Server bind port")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    LOG_FORMAT: LogFormat = Field(default=LogFormat.JSON, description="Log output format")

    # ── Database (optional) ────────────────────────────────────────
    DATABASE_URL: Optional[str] = Field(default=None, description="PostgreSQL connection URL")
    REDIS_URL: Optional[str] = Field(default=None, description="Redis connection URL")

    # ── Validators ─────────────────────────────────────────────────
    @field_validator("SEMANTIC_THRESHOLD", "FACT_THRESHOLD")
    @classmethod
    def validate_critical_thresholds(cls, v: float, info) -> float:
        """Semantic and fact thresholds should not be set too low in production."""
        if v < 0.5:
            import warnings
            warnings.warn(
                f"{info.field_name}={v} is dangerously low. "
                f"This could allow meaning drift or factual errors.",
                UserWarning,
                stacklevel=2,
            )
        return v

    def has_openai(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY)

    def has_anthropic(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.ANTHROPIC_API_KEY)

    def has_google(self) -> bool:
        """Check if Google API key is configured."""
        return bool(self.GOOGLE_API_KEY)

    def has_any_llm(self) -> bool:
        """Check if at least one LLM provider is configured."""
        return self.has_openai() or self.has_anthropic() or self.has_google()

    def get_available_providers(self) -> list[str]:
        """Return list of configured LLM providers."""
        providers = []
        if self.has_openai():
            providers.append("openai")
        if self.has_anthropic():
            providers.append("anthropic")
        if self.has_google():
            providers.append("google")
        return providers


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns the same Settings instance on every call (singleton pattern).
    Call this instead of constructing Settings() directly.
    """
    return Settings()
