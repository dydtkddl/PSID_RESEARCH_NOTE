# -*- coding: utf-8 -*-
"""
Application Configuration
- Environment-based settings
- Security defaults
- Database configuration
"""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "Research Platform"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8151
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    
    # Database (SQLite for development)
    DATABASE_URL: str = "sqlite:///./data/research_platform.db"
    DATABASE_ECHO: bool = False
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Session / Security
    SESSION_SECRET: str = "CHANGE_THIS_SESSION_SECRET_IN_PRODUCTION"
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Password Hashing
    PBKDF2_ITERATIONS: int = 200_000
    
    # Features
    ENABLE_REGISTRATION: bool = True
    ENABLE_SSO: bool = False
    REQUIRE_EMAIL_VERIFICATION: bool = False
    
    # URL Prefix for reverse proxy (e.g., "/research")
    ROOT_PATH: str = "/research"
    
    # Initial Superuser
    SUPERUSER_EMAIL: Optional[str] = "admin@localhost"
    SUPERUSER_PASSWORD: Optional[str] = "admin123"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: List[str] = [
        ".md", ".txt", ".pdf", ".docx",
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
        ".csv", ".json", ".yaml", ".yml"
    ]
    
    # Markdown
    MD_EXTENSIONS: List[str] = [
        "tables", "fenced_code", "codehilite", "toc",
        "footnotes", "attr_list", "md_in_html", "nl2br",
        "pymdownx.arithmatex", "pymdownx.superfences",
        "pymdownx.highlight", "pymdownx.tasklist"
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
