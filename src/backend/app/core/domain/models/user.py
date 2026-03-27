from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from ..value_objects import UserName, UserRole


class User:
    def __init__(
        self,
        user_id: UUID,
        username: UserName,
        hashed_password: str | None,
        role: UserRole,
        created_at: datetime,
    ) -> None:
        """uploading an existing user"""
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at

    @classmethod
    def create(cls, username: str, hashed_password: str | None) -> Self:
        """new user factory"""
        user_id = uuid4()
        username_ = UserName(value=username)
        role = UserRole(value="User")
        created_at = datetime.now()

        return cls(user_id, username_, hashed_password, role, created_at)
