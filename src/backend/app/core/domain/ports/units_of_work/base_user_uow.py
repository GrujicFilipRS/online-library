from .....shared.domain.ports import BaseRefreshSessionStorage, BaseUnitOfWork
from ..repositories import BaseUserRepository
from ..services import BaseAuthService, BaseUserService


class BaseUserUnitOfWork(BaseUnitOfWork):
    user_repo: BaseUserRepository
    user_service: BaseUserService
    refresh_sess_store: BaseRefreshSessionStorage
    auth_service: BaseAuthService
