from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

# from ....app.core.domain.exceptions import (
#    DomainError,
# )
from .logging import StructuredLogger
from .traceid_middleware import TraceIDMiddleware, trace_id_var


class ErrorResponse(BaseModel):
    error: dict[str, Any]


class AppError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


def _payload(
    *,
    request: Request,
    code: str,
    message: str,
    status_code: int,
    details: Any = None,
) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "success": False,
        "error": {
            "details": details,
            "request_id": trace_id_var.get(),
            "path": request.url.path,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    }


# def map_domain_error(exc: DomainError) -> AppError:
#    return AppError(
#        code=exc.__class__.__name__,
#        message=exc.message,
#        status_code=400,
#    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_payload(
            request=request,
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    code = f"HTTP_{exc.status_code}"
    message = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    return JSONResponse(
        status_code=exc.status_code,
        content=_payload(
            request=request,
            code=code,
            message=message,
            status_code=exc.status_code,
            details=exc.detail if not isinstance(exc.detail, str) else None,
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_payload(
            request=request,
            code="VALIDATION_ERROR",
            message="request validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=exc.errors(),
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = trace_id_var.get()

    StructuredLogger.exception(
        "unhandled exception",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_payload(
            request=request,
            code="INTERNAL_SERVER_ERROR",
            message="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=None,
        ),
    )


# async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
#    app_error = map_domain_error(exc)
#    return await app_error_handler(request, app_error)


def setup_error_handling(app: FastAPI) -> None:
    app.add_middleware(TraceIDMiddleware)

    app.add_exception_handler(AppError, app_error_handler)  # type: ignore
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(Exception, unhandled_exception_handler)
    # app.add_exception_handler(DomainError, domain_exception_handler)  # type: ignore
