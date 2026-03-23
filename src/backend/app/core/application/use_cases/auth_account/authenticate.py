from collections.abc import Callable

from ....domain.models import AuthAccount
from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ....domain.value_objects import AuthProvider, AuthProviderUserId


class AutheticateUseCase:
    def __init__(
        self, auth_account_uow_factory: Callable[[], BaseAuthAccountUnitOfWork]
    ):
        self.auth_account_uow_factory = auth_account_uow_factory

    async def execute(
        self, provider: AuthProvider, provider_user_id: AuthProviderUserId
    ) -> AuthAccount:
        async with self.auth_account_uow_factory() as uow:
            auth_account = (
                await uow.auth_account_service.authenticate_via_auth_provider(
                    provider, provider_user_id
                )
            )
            return auth_account
