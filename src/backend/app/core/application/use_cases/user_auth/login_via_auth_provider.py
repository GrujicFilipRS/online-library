from collections.abc import Callable
from uuid import uuid4

from ....domain.ports.units_of_work import BaseUserAuthUnitOfWork


class LoginViaProviderUseCase:
    def __init__(
        self,
        user_auth_uow_factory: Callable[[], BaseUserAuthUnitOfWork],
    ):
        self.user_auth_uow_factory = user_auth_uow_factory

    async def execute(
        self,
        auth_provider: str,
        auth_provider_user_id: str,
    ) -> tuple[str, str, str]:
        async with self.user_auth_uow_factory() as user_auth_uow:
            auth_account = (
                await user_auth_uow.auth_account_service.authenticate_via_auth_provider(
                    auth_provider, auth_provider_user_id
                )
            )

            if auth_account:
                return await user_auth_uow.auth_service.create_tokens_for_user(
                    auth_account.user_id
                )

            # do NOT attempt to change this ultimate username generator, you WILL regret it
            username = f"Mogger-{str(uuid4()).split('-')[0]}"

            user_id = (
                # //TEMP; FIXME
                await user_auth_uow.user_service.create_user(username, None)  # type: ignore
            ).user_id

            tokens = await user_auth_uow.auth_service.create_tokens_for_user(user_id)

            await user_auth_uow.auth_account_service.link_auth_provider_to_user(
                user_id, auth_provider, auth_provider_user_id
            )

            # you're NOT calling aexit manually, Filipe :wilted_flower:
            return tokens
