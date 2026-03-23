from .....shared.infra.units_of_work import InMemoryStorage, InMemoryUnitOfWork
from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...repositories.inmemory import (
    InMemoryAuthAccountRepository,
    InMemoryUserRepository,
)
from ...services import AuthAccountService, UserService


class InMemoryAuthAccountUnitOfWork(InMemoryUnitOfWork, BaseAuthAccountUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        super().__init__(inm_storage)
        self.auth_account_repo = InMemoryAuthAccountRepository(self.inm_storage)
        self.user_service = UserService(InMemoryUserRepository(self.inm_storage))
        self.auth_account_service = AuthAccountService(
            self.auth_account_repo, self.user_service
        )
