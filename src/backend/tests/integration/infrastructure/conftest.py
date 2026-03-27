from collections.abc import AsyncGenerator
from typing import Any

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.backend.app.core.infrastructure.db_models import *
from src.backend.app.core.infrastructure.repositories.sqlal import (
    SqlAlchemyAuthAccountRepository,
    SqlAlchemyUserRepository,
)
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
async def user_repo(db_sess):
    return SqlAlchemyUserRepository(db_sess)


@pytest.fixture
async def auth_account_repo(db_sess):
    return SqlAlchemyAuthAccountRepository(db_sess)
