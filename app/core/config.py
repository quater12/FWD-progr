"""Application settings (Pydantic Settings)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads configuration from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi_db"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi_test"

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Project"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
