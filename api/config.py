"""
Configuration settings for the Task Management API.

Provides centralized configuration for:
- Database connection
- API settings
- File paths
"""

from pathlib import Path
from typing import Optional
from functools import lru_cache


class Settings:
    """Application settings."""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    SUBJECTS_PATH: Path = PROJECT_ROOT / "subjects"

    # Database settings
    DATABASE_URL: str = f"sqlite:///{PROJECT_ROOT / 'tasks.db'}"

    # API settings
    API_TITLE: str = "Educational Material Task Management API"
    API_DESCRIPTION: str = """
    API for managing educational material generation tasks.

    Tracks subjects, topics, generated materials, and generation tasks
    for the Educational Material Automation System.
    """
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # CORS settings (for future web frontend)
    CORS_ORIGINS: list[str] = ["*"]

    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings instance
    """
    return Settings()


# Convenience exports
settings = get_settings()
