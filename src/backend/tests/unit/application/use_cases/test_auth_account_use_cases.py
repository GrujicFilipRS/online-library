from uuid import uuid4

from src.backend.app.core.domain.models import AuthAccount


async def test_authenticate_use_case(
    register_via_password, link_auth_provider, authenticate
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    provider = "github"
    provider_user_id = uuid4().hex
    auth_account = await link_auth_provider.execute(
        user.user_id, provider, provider_user_id
    )

    get_auth_account = await authenticate.execute(provider, provider_user_id)

    assert isinstance(get_auth_account, AuthAccount)
    assert get_auth_account.auth_account_id == auth_account.auth_account_id
