from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthAccountDTO(BaseModel):
    id: UUID
    user_id: UUID
    provider: str
    provider_user_id: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True, frozen=True, str_strip_whitespace=True
    )
