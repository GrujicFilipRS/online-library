from collections.abc import Callable
from uuid import UUID

from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork


class ChangeAuthProviderIdentifierUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self,
        user_id: UUID,
        auth_provider: str,
        new_auth_provider_user_id: str,
    ) -> None:
        async with self.auth_account_uow_factory() as auth_account_uow:
            await auth_account_uow.auth_account_service.change_auth_provider_identifier(
                user_id, auth_provider, new_auth_provider_user_id
            )
