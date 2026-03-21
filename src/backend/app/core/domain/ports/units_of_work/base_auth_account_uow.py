from .....shared.domain.ports import BaseUnitOfWork
from ..repositories import BaseAuthAccountRepository
from ..services import BaseAuthAccountService


class BaseAuthAccuontUnitOfWork(BaseUnitOfWork):
    auth_account_repo: BaseAuthAccountRepository
    auth_account_service: BaseAuthAccountService
