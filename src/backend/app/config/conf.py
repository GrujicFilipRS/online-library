# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from os import getenv

from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = (
    "DATABASE_URL_DEV",
    "DATABASE_URL_PROD",
    "REDIS_URL",
    "APP_NAME",
    "APP_DESCRIPTION",
    "APP_VERSION",
    "APP_SECRET_KEY",
)

TEST_MODE: bool = getenv("TEST_MODE", "false").lower() == "true"


def require_env(name: str) -> str:
    value = getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


raise_exc: bool = False
missing_vars: list[str] = []

for var in REQUIRED_ENV_VARS:
    try:
        require_env(var)
    except RuntimeError:
        if TEST_MODE is None:
            raise_exc = True
        missing_vars.append(var)

if raise_exc:
    raise Exception(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )


class Config:
    def __new__(cls):
        raise TypeError("Config is a static configuration class")

    DATABASE_URL_DEV: str = require_env("DATABASE_URL_DEV")
    DATABASE_URL_PROD: str = require_env("DATABASE_URL_PROD")
    PRJ_DEV_MODE: bool = getenv("PRJ_DEV_MODE", "true").lower() == "true"

    REDIS_URL: str = require_env("REDIS_URL")

    APP_NAME: str = require_env("APP_NAME")
    APP_DESCRIPTION: str = require_env("APP_DESCRIPTION")
    APP_VERSION: str = require_env("APP_VERSION")
    ENABLE_API_DOCS: bool = getenv("ENABLE_API_DOCS", "true").lower() == "true"

    DATABASE_URL: str = DATABASE_URL_DEV if PRJ_DEV_MODE else DATABASE_URL_PROD
    FRONTEND_URL: str = getenv("FRONTEND_URL", "http://localhost:5173")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 24))
    APP_SECRET_KEY: str = require_env("APP_SECRET_KEY")
