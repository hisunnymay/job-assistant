import pytest

from app.core.config import get_settings


def test_settings_read_database_url_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    database_url = "postgresql+psycopg://example:example@localhost:5432/example"
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()

    assert get_settings().database_url == database_url

    get_settings.cache_clear()
