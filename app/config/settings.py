# app/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Vendor Recommendation API"
    ENVIRONMENT: str = Field(default="development")

    # Database - Neon PostgreSQL
    DATABASE_URL: str = Field(..., description="PostgreSQL connection string")

    # Redis for ARQ
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # AI - Gemini
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API Key")
    GEMINI_EMBEDDING_MODEL: str = Field(default="gemini-embedding-2")
    GEMINI_EMBEDDING_DIMENSIONS: int = Field(default=768)
    GEMINI_GENERATION_MODEL: str = Field(default="gemini-3.1-flash-lite")

    # Local storage
    UPLOAD_DIR: str = Field(default="uploads")
    REPORTS_DIR: str = Field(default="reports")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def async_database_url(self) -> str:
        """Ensure the DB URL uses the asyncpg driver."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL


# Instantiate settings to be imported across the app
settings = Settings()