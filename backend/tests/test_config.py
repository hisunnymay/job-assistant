from collections.abc import Callable
from typing import cast

import pytest
from pydantic import SecretStr, ValidationError

from app.ai.ark import ArkAIService
from app.ai.dependencies import create_ai_service
from app.ai.mock import MockAIService
from app.core.config import Settings, get_settings


def isolated_settings(**values: object) -> Settings:
    values.setdefault("ai_provider", "mock")
    values.setdefault("ark_api_key", None)
    settings_constructor = cast(Callable[..., Settings], Settings)
    return settings_constructor(_env_file=None, **values)


def test_settings_read_database_url_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    database_url = "postgresql+psycopg://example:example@localhost:5432/example"
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()

    assert get_settings().database_url == database_url

    get_settings.cache_clear()


def test_mock_provider_is_the_safe_default() -> None:
    settings = isolated_settings()

    assert Settings.model_fields["ai_provider"].default == "mock"
    assert settings.ai_provider == "mock"
    assert settings.ark_api_key is None
    assert settings.ark_request_timeout_seconds == 180
    assert isinstance(create_ai_service(settings), MockAIService)


def test_ark_provider_requires_a_non_empty_backend_secret() -> None:
    with pytest.raises(ValidationError, match="ARK_API_KEY is required"):
        isolated_settings(ai_provider="ark")

    with pytest.raises(ValidationError, match="ARK_API_KEY is required"):
        isolated_settings(ai_provider="ark", ark_api_key=SecretStr("   "))


def test_valid_ark_settings_create_the_real_adapter_without_exposing_secret() -> None:
    settings = isolated_settings(
        ai_provider="ark",
        ark_api_key=SecretStr("test-only-secret"),
    )

    assert isinstance(create_ai_service(settings), ArkAIService)
    assert "test-only-secret" not in repr(settings)


@pytest.mark.parametrize(
    "settings_override",
    [
        {"ark_base_url": "not-a-url"},
        {"ark_base_url": "http://ark.example/api/v3"},
        {"ark_base_url": "https://user:password@ark.example/api/v3"},
        {"ark_base_url": "https://ark.example/api/v3?secret=value"},
        {"ark_base_url": "https://ark.example/api/v3/chat/completions"},
        {"ark_base_url": "https://ark.example/api/v3/responses"},
        {"ark_model": "   "},
        {"ark_request_timeout_seconds": 0},
        {"ark_request_timeout_seconds": -1},
        {"ark_request_timeout_seconds": float("inf")},
        {"ark_request_timeout_seconds": float("nan")},
    ],
)
def test_invalid_ark_configuration_is_rejected(
    settings_override: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        isolated_settings(**settings_override)
