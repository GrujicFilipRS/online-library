from collections.abc import Callable
from uuid import UUID

from ...domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...domain.value_objects import Provider, ProviderUserId


class ChangeProviderIdentifierUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self, user_id: UUID, provider: Provider, new_provider_user_id: ProviderUserId
    ) -> None:
        async with self.auth_account_uow_factory() as uow:
            await uow.auth_account_service.change_provider_identifier(
                user_id, provider, new_provider_user_id
            )
            await uow.commit()
