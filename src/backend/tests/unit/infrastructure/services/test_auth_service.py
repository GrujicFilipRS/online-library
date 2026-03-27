import pytest

from src.backend.app.core.domain.exceptions import (
    InvalidCredentialsError,
)
from src.backend.app.core.infrastructure.services import AuthService, UserService
from src.backend.app.shared.infrastructure.refresh_sess_stores import (
    InMemoryRefreshSessionStorage,
)


@pytest.fixture
async def refresh_sess_store(inm_storage):
    return InMemoryRefreshSessionStorage(inm_storage)


@pytest.fixture
async def auth_service(user_repo, refresh_sess_store):
    return AuthService(user_repo, refresh_sess_store)


@pytest.fixture
async def user_service(user_repo):
    return UserService(user_repo)


async def test_login_user_successfully(auth_service, user_service):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    access_token, refresh_token, csrf_token = await auth_service.login_user(
        user, password
    )
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert isinstance(csrf_token, str)


async def test_login_user_invalid_password_raises(auth_service, user_service):
    username = "ril737"
    password = "73"

    user = await user_service.create_user(username, password)

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login_user(user, "37")
