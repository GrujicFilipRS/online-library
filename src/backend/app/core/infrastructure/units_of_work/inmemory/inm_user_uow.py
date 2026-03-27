from .....shared.infrastructure.inm_storage import InMemoryStorage
from .....shared.infrastructure.refresh_sess_stores import InMemoryRefreshSessionStorage
from .....shared.infrastructure.units_of_work import InMemoryUnitOfWork
from ....domain.ports.units_of_work import BaseUserUnitOfWork
from ...repositories.inmemory import InMemoryUserRepository
from ...services import AuthService, UserService


class InMemoryUserUnitOfWork(InMemoryUnitOfWork, BaseUserUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        super().__init__(inm_storage)
        self.user_repo = InMemoryUserRepository(self.inm_storage)
        self.user_service = UserService(self.user_repo)
        self.refresh_sess_store = InMemoryRefreshSessionStorage(self.inm_storage)
        self.auth_service = AuthService(self.user_repo, self.refresh_sess_store)
