from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from ..value_objects import Provider, ProviderUserId


class AuthAccount:
    def __init__(
        self,
        account_id: UUID,
        user_id: UUID,
        provider: Provider,
        provider_user_id: ProviderUserId,
        created_at: datetime,
    ) -> None:
        self.id = account_id
        self.user_id = user_id
        self.provider = provider
        self.provider_user_id = provider_user_id
        self.created_at = created_at
        return

    @classmethod
    def create(cls, user_id: UUID, provider: str, provider_user_id: str) -> Self:
        account_id = uuid4()
        created_at = datetime.now()
        provider_vo = Provider(value=provider)
        provider_user_id_vo = ProviderUserId(value=provider_user_id)
        return cls(account_id, user_id, provider_vo, provider_user_id_vo, created_at)
