from .....shared.infrastructure.inm_storage import InMemoryStorage
from .....shared.infrastructure.units_of_work import InMemoryUnitOfWork
from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...repositories.inmemory import InMemoryAuthAccountRepository
from ...services import AuthAccountService


class InMemoryAuthAccountUnitOfWork(InMemoryUnitOfWork, BaseAuthAccountUnitOfWork):
    def __init__(self, inm_storage: InMemoryStorage):
        super().__init__(inm_storage)
        self.auth_account_repo = InMemoryAuthAccountRepository(self.inm_storage)
        self.auth_account_service = AuthAccountService(self.auth_account_repo)
