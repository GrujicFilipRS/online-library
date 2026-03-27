from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from .....shared.utils import Database


class DBSessionProvider(Provider):
    """Provider for embedding the database session in the application"""

    def __init__(self, db_sess: AsyncSession | None = None):
        super().__init__()
        self._db_sess = db_sess

    @provide(scope=Scope.REQUEST)
    async def provide_db_sess(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Provides an asynchronous database session for each request.
        Used inside the async with context manager.
        """
        if self._db_sess:
            yield self._db_sess
        else:
            async with Database.get_session() as session:
                yield session
