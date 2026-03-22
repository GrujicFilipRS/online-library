from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthAccountDTO(BaseModel):
    auth_account_id: UUID
    user_id: UUID
    auth_provider: str
    auth_provider_user_id: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True, frozen=True, str_strip_whitespace=True
    )
