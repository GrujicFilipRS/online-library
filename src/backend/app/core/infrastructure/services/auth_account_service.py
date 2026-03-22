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
from ...domain.value_objects import Provider, ProviderUserId


class AuthAccountService(BaseAuthAccountService):
    def __init__(self, repository: BaseAuthAccountRepository):
        self.repository = repository

    async def link_provider_to_user(
        self, user_id: UUID, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount:
        existing_acc = await self.repository.get_by_provider(provider, provider_user_id)
        if existing_acc:
            raise AuthProviderAccountAlreadyInUseError()
        auth_account = AuthAccount.create(
            user_id, provider.value, provider_user_id.value
        )
        await self.repository.save(auth_account)
        return auth_account

    async def authenticate_via_provider(
        self, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount:
        auth_account = await self.repository.get_by_provider(provider, provider_user_id)
        if not auth_account:
            raise AuthProviderNotLinkedError(provider.value)
        return auth_account

    async def unlink_provider_from_user(
        self, user_id: UUID, provider: Provider
    ) -> None:
        auth_accounts = await self.repository.get_by_user_id(user_id)
        if not auth_accounts:
            raise UserNotFoundError
        auth_account = next(
            (acc for acc in auth_accounts if acc.provider == provider), None
        )
        if not auth_account:
            raise AuthProviderNotLinkedError()
        if not await self.is_unlink_safe(user_id, provider):
            raise AuthProviderUnlinkNotSafeError()
        await self.repository.delete(auth_account.id)

    async def list_user_providers(self, user_id: UUID) -> list[AuthAccount]:
        auth_accounts = await self.repository.get_by_user_id(user_id)
        return auth_accounts

    async def change_provider_identifier(
        self, user_id: UUID, provider: Provider, new_identifier: ProviderUserId
    ) -> None:
        existing_acc = await self.repository.get_by_provider(provider, new_identifier)
        if existing_acc and existing_acc.user_id != user_id:
            raise AuthProviderAccountAlreadyInUseError
        auth_accounts = await self.repository.get_by_user_id(user_id)
        if not auth_accounts:
            raise UserNotFoundError
        auth_account = next(
            (acc for acc in auth_accounts if acc.provider == provider), None
        )
        if not auth_account:
            raise AuthProviderNotLinkedError
        auth_account.provider_user_id = new_identifier
        await self.repository.save(auth_account)

    async def is_unlink_safe(self, user_id: UUID, provider: Provider) -> bool:
        auth_accounts = await self.repository.get_by_user_id(user_id)
        has_target = any(acc.provider == provider for acc in auth_accounts)
        if len(auth_accounts) > 1 and has_target:
            return True
        return False

    # TODO: add a check for the user having a password as a way to authenticate
