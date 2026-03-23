from ...domain.ports import BaseUnitOfWork
from ...utils import StructuredLogger
from .inm_storage import InMemoryStorage


class InMemoryUnitOfWork(BaseUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage
        self._logging_enabled: bool = True

    async def _commit(self) -> None:
        if self._logging_enabled:
            StructuredLogger.info("inm_uow.db_sess.committed")

    async def _rollback(self) -> None:
        # //@TODO: implement in-memory db rollback
        if self._logging_enabled:
            StructuredLogger.exception("inm_uow.db_sess.rollback")
