from .....shared.domain.ports import BaseUnitOfWork
from ..repositories import BaseAuthAccountRepository
from ..services import BaseAuthAccountService, BaseUserService


class BaseAuthAccountUnitOfWork(BaseUnitOfWork):
    auth_account_repo: BaseAuthAccountRepository
    auth_account_service: BaseAuthAccountService
    user_service: BaseUserService
