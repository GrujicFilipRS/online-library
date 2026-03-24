from fastapi import Response

from ....config import get_config

config = get_config()


class CookiesUtils:
    @staticmethod
    def set_auth_cookies(
        response: Response, access_token: str, refresh_token: str, csrf_token: str
    ) -> None:
        max_age = int(config.ACCESS_TTL.total_seconds())

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE,  # type: ignore
            domain=config.COOKIE_DOMAIN,
            path="/",
            max_age=max_age,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE,  # type: ignore
            domain=config.COOKIE_DOMAIN,
            path="/auth/refresh",
            max_age=max_age,
        )

        response.set_cookie(
            key="csrf_token",
            value=csrf_token,
            httponly=False,
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE,  # type: ignore
            domain=config.COOKIE_DOMAIN,
            path="/",
            max_age=max_age,
        )

    @staticmethod
    def clear_auth_cookies(response: Response) -> None:
        response.delete_cookie("access_token", path="/", domain=config.COOKIE_DOMAIN)
        response.delete_cookie(
            "refresh_token", path="/auth/refresh", domain=config.COOKIE_DOMAIN
        )
        response.delete_cookie("csrf_token", path="/", domain=config.COOKIE_DOMAIN)
