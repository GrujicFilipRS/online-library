from datetime import datetime
from uuid import UUID

from src.backend.app.core.domain.models import User
from src.backend.app.core.domain.value_objects import UserName, UserRole


async def test_user_create_success():
    username = "ril7373"
    hashed_password = "73"

    user = User.create(username, hashed_password)

    assert isinstance(user.user_id, UUID)
    assert isinstance(user.username, UserName)
    assert user.username.value == username
    assert user.hashed_password == hashed_password
    assert isinstance(user.role, UserRole)
    assert user.role.value == "User"
    assert isinstance(user.created_at, datetime)
