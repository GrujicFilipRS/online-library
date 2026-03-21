from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from .database import Database
from .logging import StructuredLogger

# from .redis import RedisService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Контекстный менеджер для управления временем жизни приложения FastAPI.
    Инициализирует и закрывает ресурсы при старте и остановке приложения.
    """
    StructuredLogger.setup()
    try:
        await Database.init()
        await Database.test_connection()
        # await RedisService.init()
        yield
    except Exception as e:
        StructuredLogger.exception("init.error", error=str(e))
        raise e
    finally:
        await app.state.dishka_container.close()
        await Database.close()
        # await RedisService.close()
