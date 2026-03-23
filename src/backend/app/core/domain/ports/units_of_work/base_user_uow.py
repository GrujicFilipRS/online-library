from .....shared.domain.ports import BaseUnitOfWork
from ..repositories import BaseUserRepository
from ..services import BaseAuthService, BaseUserService


class BaseUserUnitOfWork(BaseUnitOfWork):
    user_repo: BaseUserRepository
    user_service: BaseUserService
    auth_service: BaseAuthService
