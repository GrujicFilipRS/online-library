from uuid import uuid4

import pytest

from src.backend.app.core.domain.exceptions import (
    InvalidAuthProviderError,
    InvalidAuthProviderUserIdError,
    InvalidLengthError,
    InvalidRoleError,
)
from src.backend.app.core.domain.value_objects import (
    AuthProvider,
    AuthProviderUserId,
    UserName,
    UserRole,
)


async def test_username_vo_length_ok():
    assert UserName("ril737")  # minimum length is 6 chars
    assert UserName("ril73" * 5)  # maximum length is 25 chars


async def test_username_vo_invalid_length_raises():
    with pytest.raises(InvalidLengthError):
        UserName("ril73")
    with pytest.raises(InvalidLengthError):
        UserName("ril73" * 7)


async def test_user_role_vo_ok():
    assert UserRole("User")
    assert UserRole("Admin")


async def test_user_role_vo_invalid_raises():
    with pytest.raises(InvalidRoleError):
        UserRole("ril73")


async def test_auth_provider_vo_ok():
    assert AuthProvider("google")
    assert AuthProvider("github")
    assert AuthProvider("apple")


async def test_auth_provider_vo_invalid_raises():
    with pytest.raises(InvalidAuthProviderError):
        AuthProvider("ril73")


async def test_auth_provider_user_id_ok():
    assert AuthProviderUserId(uuid4().hex)  # not actual, example


async def test_auth_provider_user_id_empty_raises():
    with pytest.raises(InvalidAuthProviderUserIdError):
        AuthProviderUserId("    ")
