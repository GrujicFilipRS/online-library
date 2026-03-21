from traceback import print_exc

from ...domain.ports import BaseUnitOfWork
from .inm_storage import InMemoryStorage


class InMemoryUnitOfWork(BaseUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

    async def _commit(self) -> None:
        print("[InMemory UoW] committed")

    async def _rollback(self) -> None:
        # //@TODO: implement in-memory db rollback
        print("[InMemory UoW] warning: an exception occurred. in-memory db rolled back")
        print_exc()
