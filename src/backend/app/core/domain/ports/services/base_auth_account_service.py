from abc import ABC, abstractmethod
from uuid import UUID

from ...models import AuthAccount
from ...value_objects import AuthProvider, AuthProviderUserId


class BaseAuthAccountService(ABC):
    @abstractmethod
    async def link_auth_provider_to_user(
        self,
        user_id: UUID,
        auth_provider: AuthProvider,
        auth_provider_user_id: AuthProviderUserId,
    ) -> AuthAccount: ...

    @abstractmethod
    async def authenticate_via_auth_provider(
        self,
        auth_provider: AuthProvider,
        auth_provider_user_id: AuthProviderUserId,
    ) -> AuthAccount: ...

    @abstractmethod
    async def unlink_auth_provider_from_user(
        self,
        user_id: UUID,
        auth_provider: AuthProvider,
    ) -> None: ...

    @abstractmethod
    async def list_user_auth_providers(self, user_id: UUID) -> list[AuthAccount]: ...

    @abstractmethod
    async def change_auth_provider_identifier(
        self,
        user_id: UUID,
        auth_provider: AuthProvider,
        new_identifier: AuthProviderUserId,
    ) -> None: ...

    @abstractmethod
    async def is_unlink_safe(
        self,
        user_id: UUID,
        auth_provider: AuthProvider,
    ) -> bool: ...

    """check if user has any other ways to authenticate after unlinking"""
