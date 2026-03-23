from uuid import UUID

from ....shared.utils.auth import AuthUtils
from ...domain.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from ...domain.models import User
from ...domain.ports.repositories import BaseUserRepository
from ...domain.ports.services import BaseUserService


class UserService(BaseUserService):
    def __init__(self, user_repo: BaseUserRepository):
        self.user_repo = user_repo

    async def create_user(self, username: str, password: str) -> User:
        existing = await self.user_repo.get_by_username(username)
        if existing is not None:
            raise UserAlreadyExistsError("username already taken")
        hashed_password = await AuthUtils.hash_password(password)
        user = User.create(username, hashed_password)
        await self.user_repo.save(user)
        return user

    async def login_user(self, username: str, password: str) -> User:
        user = await self.get_user_by_username(username)
        if not await AuthUtils.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("invalid credentials")
        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("user with given id not found")
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.user_repo.get_by_username(username)
        if user is None:
            raise UserNotFoundError("user with given username not found")
        return user

    async def has_password_set(self, user_id: UUID) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user.hashed_password:
            return False
        return True
