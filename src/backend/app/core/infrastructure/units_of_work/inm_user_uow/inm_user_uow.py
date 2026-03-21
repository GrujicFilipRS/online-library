from .....shared.infra.units_of_work import InMemoryStorage, InMemoryUnitOfWork
from ....domain.ports.units_of_work import BaseUserUnitOfWork
from ...repositories.inmemory import InMemoryUserRepository
from ...services import UserService


class InMemoryUserUnitOfWork(InMemoryUnitOfWork, BaseUserUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        super().__init__(inm_storage)
        self.user_repo = InMemoryUserRepository(self.inm_storage)
        self.user_service = UserService(self.user_repo)
