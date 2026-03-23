from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .app.config import get_config
from .app.core.infrastructure.di.providers import (
    DBSessionProvider,
    RepositoryProvider,
    ServiceProvider,
    UnitOfWorkFactoryProvider,
    UseCaseProvider,
)
from .app.core.presentation.api.v1 import api_v1_router
from .app.shared.utils import lifespan, setup_error_handling

config = get_config()

app = FastAPI(
    lifespan=lifespan,
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    docs_url="/docs" if config.ENABLE_API_DOCS else None,
    redoc_url="/redoc" if config.ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if config.ENABLE_API_DOCS else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

container = make_async_container(
    DBSessionProvider(),
    RepositoryProvider(),
    ServiceProvider(),
    UnitOfWorkFactoryProvider(),
    UseCaseProvider(),
)

setup_dishka(container=container, app=app)

setup_error_handling(app)
