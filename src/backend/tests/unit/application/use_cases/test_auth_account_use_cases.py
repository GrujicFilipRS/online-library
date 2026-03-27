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


async def test_list_auth_providers_use_case(
    register_via_password, link_auth_provider, list_auth_providers
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider1 = "github"
    auth_provider_user_id1 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider1, auth_provider_user_id1
    )

    auth_provider2 = "google"
    auth_provider_user_id2 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider2, auth_provider_user_id2
    )

    auth_provider3 = "apple"
    auth_provider_user_id3 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider3, auth_provider_user_id3
    )

    auth_accounts = await list_auth_providers.execute(user.user_id)

    assert isinstance(auth_accounts, list)
    assert len(auth_accounts) == 3
