from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from ...domain.ports import BaseUnitOfWork
from ...utils import StructuredLogger


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    def __init__(self, db_sess: AsyncSession):
        self.db_sess = db_sess
        self._nested_ctx: AsyncSessionTransaction | None = None
        self._logging_enabled: bool = True

    async def __aenter__(self) -> Self:
        self._nested_ctx = self.db_sess.begin_nested()
        await self._nested_ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            await self._nested_ctx.__aexit__(exc_type, exc, tb)  # type: ignore
        finally:
            await super().__aexit__(exc_type, exc, tb)

    async def _commit(self) -> None:
        if self._nested_ctx is not None:
            await self.db_sess.commit()
            await self._nested_ctx.__aexit__(None, None, None)
            self._nested_ctx = None
            if self._logging_enabled:
                StructuredLogger.info("sqlal_uow.db_sess.committed")

    async def _rollback(self) -> None:
        if self._nested_ctx is not None:
            await self._nested_ctx.__aexit__(BaseException, BaseException(), None)
            self._nested_ctx = None
            if self._logging_enabled:
                StructuredLogger.exception("sqlal_uow.db_sess.rollback")
