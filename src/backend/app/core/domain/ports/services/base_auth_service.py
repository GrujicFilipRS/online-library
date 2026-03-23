from abc import ABC, abstractmethod

from ....domain.models import User
from ..repositories import BaseUserRepository


class BaseAuthService(ABC):
    user_repo: BaseUserRepository

    @abstractmethod
    async def login_user(self, user: User, password: str) -> tuple[str, str, str]: ...
