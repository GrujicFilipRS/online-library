from collections.abc import Callable
from uuid import UUID

from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork


class UnlinkAuthProviderUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(self, user_id: UUID, auth_provider: str) -> None:
        async with self.auth_account_uow_factory() as uow:
            has_password_set = await uow.user_service.has_password_set(user_id)
            await uow.auth_account_service.unlink_auth_provider_from_user(
                user_id, auth_provider, has_password_set
            )
