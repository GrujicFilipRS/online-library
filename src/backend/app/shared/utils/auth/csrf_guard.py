from fastapi import Header, HTTPException, Request, status

from ....config import get_config
from .auth import AuthUtils

config = get_config()


class CSRFGuard:
    _safe_methods = {"GET", "HEAD", "OPTIONS"}

    @classmethod
    async def check_origin_and_fetch_metadata(cls, request: Request) -> None:
        if request.method.upper() in cls._safe_methods:
            return

        sec_fetch_site = request.headers.get("sec-fetch-site")
        if sec_fetch_site == "cross-site":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-site request blocked",
            )

        origin = request.headers.get("origin")
        if origin is not None:
            if origin != config.API_URL:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Bad origin"
                )
            return

        referer = request.headers.get("referer")
        if referer is None or not referer.startswith(config.API_URL + "/"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Bad referer"
            )

    @classmethod
    async def _csrf_guard(
        cls,
        request: Request,
        auth_cookie_name: str,
        x_csrf_token: str | None,
    ) -> dict:
        await cls.check_origin_and_fetch_metadata(request)

        cookie_csrf = request.cookies.get("csrf_token")
        if not cookie_csrf or not x_csrf_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing"
            )

        if cookie_csrf != x_csrf_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token mismatch",
            )

        auth_cookie = request.cookies.get(auth_cookie_name)
        if not auth_cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        payload = await AuthUtils.decode_token(auth_cookie)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )

        if payload.claims.get("sid") is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session",
            )

        if not await AuthUtils.verify_csrf_token(payload.claims["sid"], cookie_csrf):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token",
            )

        return payload.claims

    @classmethod
    async def require_access_csrf(
        cls,
        request: Request,
        x_csrf_token: str | None = Header(default=None, alias="X-CSRF-Token"),
    ) -> dict:
        payload = await cls._csrf_guard(request, "access_token", x_csrf_token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return payload

    @classmethod
    async def require_refresh_csrf(
        cls,
        request: Request,
        x_csrf_token: str | None = Header(default=None, alias="X-CSRF-Token"),
    ) -> dict:
        payload = await cls._csrf_guard(request, "refresh_token", x_csrf_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return payload

    @classmethod
    async def get_current_user(cls, request: Request) -> dict:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        payload = await AuthUtils.decode_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )

        if payload.claims.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload.claims
