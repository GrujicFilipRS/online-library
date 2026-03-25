from collections.abc import Callable

from ....domain.models.user import User
from ....domain.ports.units_of_work import BaseUserUnitOfWork


class RegisterViaPasswordUseCase:
    def __init__(self, user_uow_factory: Callable[[], BaseUserUnitOfWork]):
        self.user_uow_factory = user_uow_factory

    async def execute(self, username: str, password: str) -> tuple[User, str, str, str]:
        """
        Creates a user, and returns the user, as well as all 3 tokens
        """
        async with self.user_uow_factory() as uow:
            user = await uow.user_service.create_user(username, password)
            access_token, refresh_token, csrf_token = await uow.auth_service.login_user(
                user, password
            )
            return user, access_token, refresh_token, csrf_token
