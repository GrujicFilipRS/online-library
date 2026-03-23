from collections.abc import Callable
from uuid import UUID

from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ....domain.value_objects import AuthProvider, AuthProviderUserId


class ChangeProviderIdentifierUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self,
        user_id: UUID,
        provider: AuthProvider,
        new_provider_user_id: AuthProviderUserId,
    ) -> None:
        async with self.auth_account_uow_factory() as uow:
            await uow.auth_account_service.change_auth_provider_identifier(
                user_id, provider, new_provider_user_id
            )
