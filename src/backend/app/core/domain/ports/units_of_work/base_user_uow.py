from .....shared.domain.ports import BaseUnitOfWork
from ..repositories import BaseUserRepository
from ..services import BaseUserService


class BaseUserUnitOfWork(BaseUnitOfWork):
    user_repo: BaseUserRepository
    user_service: BaseUserService
