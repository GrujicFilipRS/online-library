from abc import ABC, abstractmethod
from uuid import UUID

from ....domain.models import User
from ..repositories import BaseUserRepository


class BaseAuthService(ABC):
    user_repo: BaseUserRepository

    @abstractmethod
    async def create_tokens_for_user(self, user_id: UUID) -> tuple[str, str, str]: ...

    @abstractmethod
    async def login_user(self, user: User, password: str) -> tuple[str, str, str]: ...
