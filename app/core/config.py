from __future__ import annotations
from pathlib import Path
from datetime import timedelta
from typing import List
from pydantic import SecretStr, Field, ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    SECRET_KEY: SecretStr = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    DEBUG: bool = False
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    BACKEND_CORS_ORIGINS: List[str] = []

    @property
    def access_token_expire_delta(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    def get_secret_key(self) -> str:
        return self.SECRET_KEY.get_secret_value()


settings = Settings()
