import pytest

from src.backend.app.core.domain.exceptions import InvalidLengthError, InvalidRoleError
from src.backend.app.core.domain.value_objects import UserName, UserRole


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
