from collections.abc import AsyncGenerator
from typing import Any

import pytest
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.backend.app.core.infrastructure.di.providers import (
    DBSessionProvider,
    RepositoryProvider,
    ServiceProvider,
    UnitOfWorkFactoryProvider,
    UseCaseProvider,
)
from src.backend.app.core.presentation.api.v1 import api_v1_router
from src.backend.app.shared.utils import Base


@pytest.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, Any]:
    """Creates asynchronous database engine for tests"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def enable_sqlite_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def db_sess(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, Any]:
    """Creates new database session and reverts all changes after testing"""
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        sessionmaker = async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        async with sessionmaker() as session:
            await session.begin_nested()

            def restart_savepoint(sess, trans):
                if (
                    trans.nested
                    and not getattr(trans, "_parent", None)
                    or not trans._parent
                ):
                    sess.begin_nested()

            event.listen(
                session.sync_session, "after_transaction_end", restart_savepoint
            )

            try:
                yield session
            finally:
                event.remove(
                    session.sync_session, "after_transaction_end", restart_savepoint
                )

        await transaction.rollback()


@pytest.fixture
async def app_container(
    db_sess: AsyncSession,
) -> AsyncGenerator[AsyncContainer, Any]:
    app_container = make_async_container(
        DBSessionProvider(db_sess),
        RepositoryProvider(),
        ServiceProvider(),
        UnitOfWorkFactoryProvider(),
        UseCaseProvider(),
    )
    yield app_container
    await app_container.close()


@pytest.fixture
async def app(app_container: AsyncContainer) -> FastAPI:
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(api_v1_router)

    setup_dishka(container=app_container, app=app)
    return app


@pytest.fixture
async def httpx_client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    """Create HTTP-client for API testing."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
