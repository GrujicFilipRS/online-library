# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from os import environ, getenv

from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = (
    "DATABASE_URL_DEV",
    "DATABASE_URL_PROD",
    "APP_NAME",
    "APP_DESCRIPTION",
    "APP_VERSION",
    "APP_SECRET_KEY",
)

raise_exc: bool = False
missing_vars: list[str] = []

for var in REQUIRED_ENV_VARS:
    if var not in environ.keys():
        raise_exc = True
        missing_vars.append(var)

if raise_exc:
    raise Exception(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )


class Config:
    def __new__(cls):
        raise TypeError("Config is a static configuration class")

    DATABASE_URL_DEV = getenv("DATABASE_URL_DEV", "")
    DATABASE_URL_PROD = getenv("DATABASE_URL_PROD", "")
    PRJ_DEV_MODE = getenv("PRJ_DEV_MODE", "true").lower() == "true"

    APP_NAME = getenv("APP_NAME", "")
    APP_DESCRIPTION = getenv("APP_DESCRIPTION", "")
    APP_VERSION = getenv("APP_VERSION", "")
    ENABLE_API_DOCS = getenv("ENABLE_API_DOCS", "true").lower() == "true"

    DATABASE_URL = DATABASE_URL_DEV if PRJ_DEV_MODE else DATABASE_URL_PROD
    FRONTEND_URL = getenv("FRONTEND_URL", "http://localhost:5173")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 24))
    APP_SECRET_KEY = getenv("SECRET_KEY", "")
