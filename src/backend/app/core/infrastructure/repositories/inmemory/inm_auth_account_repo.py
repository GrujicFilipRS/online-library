from uuid import UUID

from .....shared.infra.inm_storage import InMemoryStorage
from ....domain.models import AuthAccount
from ....domain.ports.repositories import BaseAuthAccountRepository
from ....domain.value_objects import AuthProvider, AuthProviderUserId


class InMemoryAuthAccountRepository(BaseAuthAccountRepository):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

    async def get_by_id(self, auth_account_id: UUID) -> AuthAccount | None:
        return next(
            (
                acc
                for acc in self.inm_storage.auth_accounts
                if acc.auth_account_id == auth_account_id
            ),
            None,
        )

    async def get_by_user_id(self, user_id: UUID) -> list[AuthAccount]:
        return [acc for acc in self.inm_storage.auth_accounts if acc.user_id == user_id]

    async def get_by_auth_provider(
        self,
        auth_provider: AuthProvider,
        auth_provider_user_id: AuthProviderUserId,
    ) -> AuthAccount | None:
        return next(
            (
                acc
                for acc in self.inm_storage.auth_accounts
                if acc.auth_provider == auth_provider
                and acc.auth_provider_user_id == auth_provider_user_id
            ),
            None,
        )

    async def save(self, auth_account: AuthAccount) -> None:
        existing_index = next(
            (
                i
                for i, acc in enumerate(self.inm_storage.auth_accounts)
                if acc.auth_account_id == auth_account.auth_account_id
            ),
            None,
        )
        if existing_index is None:
            self.inm_storage.auth_accounts.append(auth_account)
            return None
        self.inm_storage.auth_accounts[existing_index] = auth_account

    async def delete(self, auth_account: AuthAccount) -> None:
        self.inm_storage.auth_accounts = [
            account
            for account in self.inm_storage.auth_accounts
            if account.auth_account_id != auth_account.auth_account_id
        ]
