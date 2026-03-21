from uuid import UUID
from abc import ABC, abstractmethod

from ...models import AuthAccount
from ...value_objects import Provider, ProviderUserId

class BaseAuthAccountRepository(ABC):
    @abstractmethod
    async def get_by_id(self, account_id: UUID) -> AuthAccount | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[AuthAccount] | None: ...

    @abstractmethod
    async def get_by_provider(self, provider: Provider, provider_user_id: ProviderUserId) -> AuthAccount | None: ...

    @abstractmethod
    async def save(self, auth_account: AuthAccount) -> None: ...

    @abstractmethod
    async def delete(self, account_id: UUID) -> None: ...

