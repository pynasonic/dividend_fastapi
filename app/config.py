# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from functools import lru_cache


class _Settings(BaseSettings):
    # Settings must not be instantiated directly.
    # Always use get_settings_singleton() to access application configuration.
    #     Settings 是实现细节，不是公共 API
    # 公共 API 只有 get_settings_singleton()
    OPENAI_API_KEY: Optional[str] = None
    SERPERDEV_API_KEY: Optional[str] = None
    TAVILY_API_KEY: str = "ff"
    ALPHAVANTAGE_API_KEY:  str = "ff"
    EOD_API_KEY:  str = "ff"
    FINNHUB_API_KEY:  str = "ff"

    # Database
    DIV_ASYNC: str = "postgresql+asyncpg://username:pwd@local/icedb"
    DIV_SYNC: str = "postgresql://postgres:password@localhost/invo"

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False


    # Seed Data
    SEED_DATA: bool = True  # Whether to seed data on startup
    SEED_TYPE: str = "full"  # 'full', 'test', or 'none'
    SEED_SAMPLE_SIZE: int = 10  # Number of sample records to create

    # Application
    PROJECT_NAME: str = "AIDividend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Dividend investing, systematically enhanced."
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

@lru_cache()
def get_settings_singleton()-> _Settings:
    return _Settings()
