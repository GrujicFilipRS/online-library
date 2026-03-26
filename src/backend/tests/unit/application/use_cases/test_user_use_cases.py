from src.backend.app.core.domain.models import User


async def test_register_and_login_via_password_use_cases(
    register_via_password, login_via_password
):
    username = "ril737"
    password = "73"
    (
        user,
        login_access_token,
        login_refresh_token,
        login_csrf_token,
    ) = await register_via_password.execute(username, password)

    assert isinstance(user, User)
    assert isinstance(login_access_token, str)
    assert isinstance(login_refresh_token, str)
    assert isinstance(login_csrf_token, str)

    access_token, refresh_token, csrf_token = await login_via_password.execute(
        username, password
    )

    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert isinstance(csrf_token, str)
