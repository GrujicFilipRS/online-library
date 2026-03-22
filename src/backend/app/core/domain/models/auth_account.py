from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from ..value_objects import AuthProvider, AuthProviderUserId


class AuthAccount:
    def __init__(
        self,
        auth_account_id: UUID,
        user_id: UUID,
        auth_provider: AuthProvider,
        auth_provider_user_id: AuthProviderUserId,
        created_at: datetime,
    ) -> None:
        self.auth_account_id = auth_account_id
        self.user_id = user_id
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id
        self.created_at = created_at
        return

    @classmethod
    def create(
        cls,
        user_id: UUID,
        auth_provider: str,
        auth_provider_user_id: str,
    ) -> Self:
        auth_account_id = uuid4()
        created_at = datetime.now()
        auth_provider_vo = AuthProvider(value=auth_provider)
        auth_provider_user_id_vo = AuthProviderUserId(value=auth_provider_user_id)
        return cls(
            auth_account_id,
            user_id,
            auth_provider_vo,
            auth_provider_user_id_vo,
            created_at,
        )
