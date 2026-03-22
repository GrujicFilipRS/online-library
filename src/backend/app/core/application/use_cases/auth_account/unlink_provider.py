from collections.abc import Callable
from uuid import UUID

from ...domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...domain.value_objects import AuthProvider


class UnlinkProviderUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(self, user_id: UUID, provider: AuthProvider) -> None:
        async with self.auth_account_uow_factory() as uow:
            await uow.auth_account_service.unlink_provider_from_user(user_id, provider)
