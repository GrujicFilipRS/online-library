from uuid import uuid4

import pytest

from src.backend.app.core.domain.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.backend.app.core.infrastructure.services import UserService


@pytest.fixture
async def user_service(user_repo):
    return UserService(user_repo)


async def test_create_and_get_user_successfully(user_service):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    get_user = await user_service.get_user_by_id(user.user_id)

    assert get_user.username.value == user.username.value
    assert get_user.hashed_password == user.hashed_password
    assert get_user.role.value == user.role.value
    assert get_user.created_at == user.created_at


async def test_create_user_with_duplicate_name_raises(user_service):
    username = "ril737"
    password = "73"

    await user_service.create_user(username, password)

    with pytest.raises(UserAlreadyExistsError):
        await user_service.create_user(username, password)


async def test_get_nonexistent_user_raises(user_service):
    with pytest.raises(UserNotFoundError):
        await user_service.get_user_by_id(uuid4())
    with pytest.raises(UserNotFoundError):
        await user_service.get_user_by_username("ril737")


async def test_user_has_password_set(user_service):
    username = "ril737"
    password = "73"

    user = await user_service.create_user(username, password)
    assert await user_service.has_password_set(user.user_id) is True

    user.hashed_password = None
    assert await user_service.has_password_set(user.user_id) is False
