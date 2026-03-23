from collections.abc import Callable

from ....domain.ports.units_of_work import BaseUserUnitOfWork
from ....domain.models.user import User

from .....shared.utils.auth import AuthUtils


class RegisterViaPasswordUseCase:
    def __init__(
        self, user_uow_factory: Callable[[], BaseUserUnitOfWork]
    ):
        self.user_uow_factory = user_uow_factory

    async def execute(self, username: str, password: str) -> User:
        async with self.user_uow_factory() as uow:
            hashed_password = await AuthUtils.hash_password(password)
            user = await uow.user_service.create_user(username, hashed_password)
            return user