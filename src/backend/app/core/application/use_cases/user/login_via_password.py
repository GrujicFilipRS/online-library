from collections.abc import Callable

from ....domain.ports.units_of_work import BaseUserUnitOfWork


class LoginViaPasswordUseCase:
    def __init__(self, user_uow_factory: Callable[[], BaseUserUnitOfWork]):
        self.user_uow_factory = user_uow_factory

    async def execute(self, username: str, password: str) -> tuple[str, str, str]:
        async with self.user_uow_factory() as uow:
            user = await uow.user_service.get_user_by_username(username)
            access_token, refresh_token, csrf_token = await uow.auth_service.login_user(
                user, password
            )
            return access_token, refresh_token, csrf_token
