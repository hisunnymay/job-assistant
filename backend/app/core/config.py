from functools import lru_cache
from typing import Annotated, Literal, Self
from urllib.parse import urlparse

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["development", "test", "production"] = "development"
    database_url: str = (
        "postgresql+psycopg://job_assistant:job_assistant@localhost:5432/job_assistant"
    )
    frontend_origin: str = "http://localhost:5173"
    ai_provider: Literal["mock", "ark"] = "mock"
    ark_api_key: SecretStr | None = None
    ark_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    ark_model: str = "doubao-seed-2-1-pro-260628"
    ark_request_timeout_seconds: Annotated[
        float,
        Field(gt=0, allow_inf_nan=False),
    ] = 180.0

    @field_validator("ark_base_url")
    @classmethod
    def validate_ark_base_url(cls, value: str) -> str:
        normalized = value.strip().rstrip("/")
        parsed = urlparse(normalized)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("ARK_BASE_URL must be an HTTPS API base URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("ARK_BASE_URL must not contain credentials, a query, or a fragment")
        if normalized.endswith(("/chat/completions", "/responses")):
            raise ValueError("ARK_BASE_URL must not include the operation path")
        return normalized

    @field_validator("ark_model")
    @classmethod
    def validate_ark_model(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("ARK_MODEL must not be empty")
        return normalized

    @model_validator(mode="after")
    def require_ark_key_for_real_provider(self) -> Self:
        if self.ai_provider == "ark" and (
            self.ark_api_key is None or not self.ark_api_key.get_secret_value().strip()
        ):
            raise ValueError("ARK_API_KEY is required when AI_PROVIDER=ark")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
