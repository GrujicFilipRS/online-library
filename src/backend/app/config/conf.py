# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # required
    APP_NAME: str = Field(min_length=1)
    APP_DESCRIPTION: str = Field(min_length=1)
    APP_VERSION: str = Field(min_length=1)
    APP_SECRET_KEY: SecretStr

    DATABASE_URL_DEV: str = Field(min_length=1)
    DATABASE_URL_PROD: str = Field(min_length=1)
    REDIS_URL: str = Field(min_length=1)

    # optional
    PRJ_DEV_MODE: bool = True
    ENABLE_API_DOCS: bool = True
    FRONTEND_URL: str = "http://localhost:5173"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24

    @property
    def DATABASE_URL(self) -> str:  # noqa: N802
        return self.DATABASE_URL_DEV if self.PRJ_DEV_MODE else self.DATABASE_URL_PROD

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore
