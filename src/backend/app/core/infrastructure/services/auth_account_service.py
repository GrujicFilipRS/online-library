from uuid import UUID

from ...domain.exceptions import (
    AuthProviderAccountAlreadyInUseError,
    AuthProviderNotLinkedError,
    AuthProviderUnlinkNotSafeError,
    UserNotFoundError,
)
from ...domain.models import AuthAccount
from ...domain.ports.repositories import BaseAuthAccountRepository
from ...domain.ports.services import BaseAuthAccountService
from ...domain.value_objects import AuthProviderUserId


class AuthAccountService(BaseAuthAccountService):
    def __init__(self, auth_account_repository: BaseAuthAccountRepository):
        self.auth_account_repository = auth_account_repository

    async def link_auth_provider_to_user(
        self,
        user_id: UUID,
        auth_provider: str,
        auth_provider_user_id: str,
    ) -> AuthAccount:
        existing_acc = await self.auth_account_repository.get_by_auth_provider(
            auth_provider, auth_provider_user_id
        )
        if existing_acc:
            raise AuthProviderAccountAlreadyInUseError()

        auth_account = AuthAccount.create(user_id, auth_provider, auth_provider_user_id)
        await self.auth_account_repository.save(auth_account)
        return auth_account

    async def authenticate_via_auth_provider(
        self,
        auth_provider: str,
        auth_provider_user_id: str,
    ) -> AuthAccount:
        auth_account = await self.auth_account_repository.get_by_auth_provider(
            auth_provider, auth_provider_user_id
        )
        if not auth_account:
            raise AuthProviderNotLinkedError(auth_provider)

        return auth_account

    async def unlink_auth_provider_from_user(
        self,
        user_id: UUID,
        auth_provider: str,
        has_password_set: bool,
    ) -> None:
        auth_accounts = await self.auth_account_repository.get_by_user_id(user_id)
        if not auth_accounts:
            raise UserNotFoundError()

        auth_account = next(
            (acc for acc in auth_accounts if acc.auth_provider.value == auth_provider),
            None,
        )

        if not auth_account:
            raise AuthProviderNotLinkedError()

        if (
            not await self.is_unlink_safe(user_id, auth_provider)
            and not has_password_set
        ):
            raise AuthProviderUnlinkNotSafeError()

        await self.auth_account_repository.delete(auth_account.auth_account_id)

    async def list_user_auth_providers(self, user_id: UUID) -> list[AuthAccount]:
        auth_accounts = await self.auth_account_repository.get_by_user_id(user_id)
        return auth_accounts

    async def change_auth_provider_identifier(
        self,
        user_id: UUID,
        auth_provider: str,
        new_identifier: str,
    ) -> None:
        existing_acc = await self.auth_account_repository.get_by_auth_provider(
            auth_provider, new_identifier
        )
        if existing_acc and existing_acc.user_id != user_id:
            raise AuthProviderAccountAlreadyInUseError()

        auth_accounts = await self.auth_account_repository.get_by_user_id(user_id)
        if not auth_accounts:
            raise UserNotFoundError()

        auth_account = next(
            (acc for acc in auth_accounts if acc.auth_provider.value == auth_provider),
            None,
        )

        if not auth_account:
            raise AuthProviderNotLinkedError()

        auth_account.auth_provider_user_id = AuthProviderUserId(new_identifier)
        await self.auth_account_repository.save(auth_account)

    async def is_unlink_safe(
        self,
        user_id: UUID,
        auth_provider: str,
    ) -> bool:
        auth_accounts = await self.auth_account_repository.get_by_user_id(user_id)
        has_target = any(
            acc.auth_provider.value == auth_provider for acc in auth_accounts
        )

        if len(auth_accounts) > 1 and has_target:
            return True

        return False
