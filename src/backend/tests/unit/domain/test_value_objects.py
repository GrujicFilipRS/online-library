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
    UserName("ril737")  # minimum length is 6 chars
    UserName("ril73" * 5)  # maximum length is 25 chars


async def test_username_vo_invalid_length_raises():
    with pytest.raises(InvalidLengthError):
        UserName("ril73")
    with pytest.raises(InvalidLengthError):
        UserName("ril73" * 7)


async def test_user_role_vo_ok():
    UserRole("User")
    UserRole("Admin")


async def test_user_role_vo_invalid_raises():
    with pytest.raises(InvalidRoleError):
        UserRole("ril73")


async def test_auth_provider_vo_ok():
    AuthProvider("google")
    AuthProvider("github")
    AuthProvider("apple")


async def test_auth_provider_vo_invalid_raises():
    with pytest.raises(InvalidAuthProviderError):
        AuthProvider("ril73")


async def test_auth_provider_user_id_ok():
    AuthProviderUserId(uuid4().hex)  # not actual, example


async def test_auth_provider_user_id_empty_raises():
    with pytest.raises(InvalidAuthProviderUserIdError):
        AuthProviderUserId("    ")
