from collections.abc import Callable

from ...domain.models import AuthAccount
from ...domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...domain.value_objects import Provider, ProviderUserId


class AutheticateUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount:
        async with self.auth_account_uow_factory() as uow:
            auth_account = await uow.auth_account_service.autheticate_via_provider(
                provider, provider_user_id
            )
            await uow.commit()
            return auth_account
