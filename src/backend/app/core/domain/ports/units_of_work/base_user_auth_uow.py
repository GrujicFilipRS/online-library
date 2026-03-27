from .....shared.domain.ports import BaseRefreshSessionStorage, BaseUnitOfWork
from ..repositories import BaseAuthAccountRepository, BaseUserRepository
from ..services import BaseAuthAccountService, BaseAuthService, BaseUserService


class BaseUserAuthUnitOfWork(BaseUnitOfWork):
    user_repo: BaseUserRepository
    user_service: BaseUserService
    refresh_sess_store: BaseRefreshSessionStorage
    auth_service: BaseAuthService
    auth_account_repo: BaseAuthAccountRepository
    auth_account_service: BaseAuthAccountService
