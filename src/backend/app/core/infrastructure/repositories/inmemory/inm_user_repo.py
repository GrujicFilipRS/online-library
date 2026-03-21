from uuid import UUID

from .....shared.infra.units_of_work import InMemoryStorage
from ....domain.models import User
from ....domain.ports.repositories import BaseUserRepository


class InMemoryUserRepository(BaseUserRepository):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

    async def get_by_id(self, user_id: UUID) -> User | None:
        for user in self.inm_storage.users:
            if user.user_id == user_id:
                return user
        return None

    async def get_by_username(self, username: str) -> User | None:
        for user in self.inm_storage.users:
            if user.username == username:
                return user
        return None

    async def save(self, user: User) -> None:
        for user_ in self.inm_storage.users:
            if user_.user_id == user.user_id:
                index = self.inm_storage.users.index(user)
                self.inm_storage.users[index] = user
                return None
        self.inm_storage.users.append(user)
        return None

    async def delete(self, user: User) -> None:
        for user_ in self.inm_storage.users:
            if user_.user_id == user.user_id:
                self.inm_storage.users.remove(user_)
                return None
        return None
