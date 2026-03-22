from abc import ABC, abstractmethod
from uuid import UUID

from ...models import AuthAccount
from ...value_objects import AuthProvider, AuthProviderUserId


class BaseAuthAccountRepository(ABC):
    @abstractmethod
    async def get_by_id(self, auth_account_id: UUID) -> AuthAccount | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[AuthAccount]: ...

    @abstractmethod
    async def get_by_auth_provider(
        self,
        auth_provider: AuthProvider,
        auth_provider_user_id: AuthProviderUserId,
    ) -> AuthAccount | None: ...

    @abstractmethod
    async def save(self, auth_account: AuthAccount) -> None: ...

    @abstractmethod
    async def delete(self, auth_account_id: UUID) -> None: ...
