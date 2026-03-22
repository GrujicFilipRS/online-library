from abc import ABC, abstractmethod
from uuid import UUID

from ...models import AuthAccount
from ...value_objects import Provider, ProviderUserId


class BaseAuthAccountService(ABC):
    @abstractmethod
    async def link_provider_to_user(
        self, user_id: UUID, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount: ...

    @abstractmethod
    async def authenticate_via_provider(
        self, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount: ...

    @abstractmethod
    async def unlink_provider_from_user(
        self, user_id: UUID, provider: Provider
    ) -> None: ...

    @abstractmethod
    async def list_user_providers(self, user_id: UUID) -> list[AuthAccount]: ...

    @abstractmethod
    async def change_provider_identifier(
        self, user_id: UUID, provider: Provider, new_identifier: ProviderUserId
    ) -> None: ...

    @abstractmethod
    async def is_unlink_safe(self, user_id: UUID, provider: Provider) -> bool: ...

    """check if user has any other ways to authenticate after unlinking"""
