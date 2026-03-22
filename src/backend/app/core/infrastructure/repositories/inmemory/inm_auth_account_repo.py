from uuid import UUID

from .....shared.infra.units_of_work import InMemoryStorage
from ....domain.models import AuthAccount
from ....domain.ports.repositories import BaseAuthAccountRepository
from ....domain.value_objects import Provider, ProviderUserId


class InMemoryAuthAccountRepository(BaseAuthAccountRepository):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

    async def get_by_id(self, account_id: UUID) -> AuthAccount | None:
        return next(
            (acc for acc in self.inm_storage.auth_accounts if acc.id == account_id),
            None,
        )

    async def get_by_user_id(self, user_id: UUID) -> list[AuthAccount]:
        return [acc for acc in self.inm_storage.auth_accounts if acc.user_id == user_id]

    async def get_by_provider(
        self, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount | None:
        return next(
            (
                acc
                for acc in self.inm_storage.auth_accounts
                if acc.provider == provider and acc.provider_user_id == provider_user_id
            ),
            None,
        )

    async def save(self, auth_account: AuthAccount) -> None:
        existing_index = next(
            (
                i
                for i, acc in enumerate(self.inm_storage.auth_accounts)
                if acc.id == auth_account.id
            ),
            None,
        )
        if existing_index is None:
            self.inm_storage.auth_accounts.append(auth_account)
            return None
        self.inm_storage.auth_accounts[existing_index] = auth_account

    async def delete(self, account_id: UUID) -> None:
        self.inm_storage.auth_accounts = [
            account
            for account in self.inm_storage.auth_accounts
            if account.id != account_id
        ]
