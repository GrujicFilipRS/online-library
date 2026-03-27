from collections.abc import Callable
from uuid import UUID

from ....domain.ports.units_of_work import BaseUserAuthUnitOfWork


class UnlinkAuthProviderUseCase:
    def __init__(self, user_auth_uow_factory: Callable[[], BaseUserAuthUnitOfWork]):
        self.user_auth_uow_factory = user_auth_uow_factory

    async def execute(self, user_id: UUID, auth_provider: str) -> None:
        async with self.user_auth_uow_factory() as user_auth_uow:
            has_password_set = await user_auth_uow.user_service.has_password_set(
                user_id
            )
            await user_auth_uow.auth_account_service.unlink_auth_provider_from_user(
                user_id, auth_provider, has_password_set
            )
