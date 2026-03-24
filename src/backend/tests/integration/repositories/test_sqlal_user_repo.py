from uuid import uuid4

from src.backend.app.core.domain.models import User
from src.backend.app.core.domain.value_objects import UserName, UserRole


async def test_save_inserts_new_user(user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    get_user = await user_repo.get_by_id(user.user_id)

    assert isinstance(get_user, User)
    assert get_user.user_id == user.user_id
    assert get_user.username.value == user.username.value
    assert get_user.hashed_password == user.hashed_password
    assert get_user.role.value == user.role.value
    assert get_user.created_at == user.created_at


async def test_save_updates_existing_user(user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    username_vo = UserName("ril373")
    role_vo = UserRole("Admin")

    user.username = username_vo
    user.role = role_vo

    await user_repo.save(user)

    get_player = await user_repo.get_by_id(user.user_id)

    assert get_player.username.value == username_vo.value
    assert get_player.role.value == role_vo.value


async def test_get_user_by_username(user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    get_user = await user_repo.get_by_username("ril737")

    assert isinstance(get_user, User)
    assert get_user.user_id == user.user_id


async def test_get_nonexistent_user_returns_none(user_repo):
    assert await user_repo.get_by_id(uuid4()) is None
    assert await user_repo.get_by_username("ril737") is None


async def test_delete_user(user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    await user_repo.delete(user)

    get_user = await user_repo.get_by_username("ril737")

    assert get_user is None
