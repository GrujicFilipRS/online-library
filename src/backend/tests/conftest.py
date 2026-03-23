import pytest

from src.backend.app.config import get_config


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setenv("APP_NAME", "")
    monkeypatch.setenv("APP_DESCRIPTION", "")
    monkeypatch.setenv("APP_VERSION", "")
    monkeypatch.setenv("APP_SECRET_KEY", "")
    monkeypatch.setenv("DATABASE_URL_DEV", "")
    monkeypatch.setenv("DATABASE_URL_PROD", "")
    monkeypatch.setenv("REDIS_URL", "")

    get_config.cache_clear()
    yield
    get_config.cache_clear()
