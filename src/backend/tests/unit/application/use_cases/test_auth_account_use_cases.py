from uuid import uuid4

from src.backend.app.core.domain.models import AuthAccount


async def test_link_auth_provider_use_case(register_via_password, link_auth_provider):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider = "github"
    auth_provider_user_id = uuid4().hex
    auth_account = await link_auth_provider.execute(
        user.user_id, auth_provider, auth_provider_user_id
    )

    assert isinstance(auth_account, AuthAccount)
    assert auth_account.user_id == user.user_id


async def test_authenticate_use_case(
    register_via_password, link_auth_provider, authenticate
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider = "github"
    auth_provider_user_id = uuid4().hex
    auth_account = await link_auth_provider.execute(
        user.user_id, auth_provider, auth_provider_user_id
    )

    get_auth_account = await authenticate.execute(auth_provider, auth_provider_user_id)

    assert isinstance(get_auth_account, AuthAccount)
    assert get_auth_account.auth_account_id == auth_account.auth_account_id


async def test_change_auth_provider_identifier_use_case(
    register_via_password,
    link_auth_provider,
    change_auth_provider_identifier,
    authenticate,
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider = "github"
    auth_provider_user_id = uuid4().hex
    auth_account = await link_auth_provider.execute(
        user.user_id, auth_provider, auth_provider_user_id
    )

    new_auth_provider_user_id = uuid4().hex
    await change_auth_provider_identifier.execute(
        user.user_id, auth_provider, new_auth_provider_user_id
    )

    get_auth_account = await authenticate.execute(
        auth_provider, new_auth_provider_user_id
    )

    assert isinstance(get_auth_account, AuthAccount)
    assert get_auth_account.auth_account_id == auth_account.auth_account_id
