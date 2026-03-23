import pytest

from src.backend.app.config import get_config


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setenv("APP_NAME", "test73")
    monkeypatch.setenv("APP_DESCRIPTION", "ril")
    monkeypatch.setenv("APP_VERSION", "7.3")
    monkeypatch.setenv(
        "APP_SECRET_KEY", "ril73-is-a-very-secret-key-that-is-at-least-32-bytes-long"
    )
    monkeypatch.setenv("DATABASE_URL_DEV", "None")
    monkeypatch.setenv("DATABASE_URL_PROD", "None")
    monkeypatch.setenv("REDIS_URL", "None")

    get_config.cache_clear()
    yield
    get_config.cache_clear()
