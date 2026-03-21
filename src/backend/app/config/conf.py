import os

from .config_loader import ConfigLoader

ConfigLoader.import_env()


class Config:
    """
    Конфигурационные параметры приложения, загружаемые из переменных окружения.
    Атрибуты доступны напрямую, без создания экземпляра класса.
    """

    DATABASE_URL_DEV = os.getenv("DATABASE_URL_DEV", "")
    DATABASE_URL_PROD = os.getenv("DATABASE_URL_PROD", "")
    PRJ_DEV_MODE = os.getenv("PRJ_DEV_MODE", "true").lower() == "true"

    DATABASE_URL = DATABASE_URL_DEV if PRJ_DEV_MODE else DATABASE_URL_PROD

    APP_NAME = os.getenv("APP_NAME", "")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "")
    APP_VERSION = os.getenv("APP_VERSION", "")
    ENABLE_API_DOCS = os.getenv("ENABLE_API_DOCS", "true").lower() == "true"

    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")
