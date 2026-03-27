from collections.abc import Callable
from uuid import UUID

from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork


class LinkAuthProviderUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self,
        user_id: UUID,
        provider: str,
        provider_user_id: str,
    ) -> None:
        async with self.auth_account_uow_factory() as auth_account_uow:
            await auth_account_uow.auth_account_service.link_auth_provider_to_user(
                user_id, provider, provider_user_id
            )
