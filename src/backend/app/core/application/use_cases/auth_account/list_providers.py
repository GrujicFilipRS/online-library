from collections.abc import Callable
from uuid import UUID

from ...domain.models import AuthAccount
from ...domain.ports.units_of_work import BaseAuthAccountUnitOfWork


class ListProvidersUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(self, user_id: UUID) -> list[AuthAccount]:
        async with self.auth_account_uow_factory() as uow:
            auth_accounts = await uow.auth_account_service.list_user_providers(user_id)
            return auth_accounts
