from abc import ABC, abstractmethod
from uuid import UUID

from ...models import User
from ..repositories import BaseUserRepository


class BaseUserService(ABC):
    user_repo: BaseUserRepository

    @abstractmethod
    async def create_user(self, username: str, hashed_password: str) -> User: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User: ...
