from src.backend.app.core.domain.models import User


async def test_register_and_login_via_password(
    register_via_password, login_via_password
):
    username = "ril737"
    password = "73"
    user = await register_via_password.execute(username, password)

    assert isinstance(user, User)

    access_token, refresh_token, csrf_token = await login_via_password.execute(
        username, password
    )

    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert isinstance(csrf_token, str)
