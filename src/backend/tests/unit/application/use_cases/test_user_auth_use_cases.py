from uuid import uuid4

import pytest

from src.backend.app.core.domain.exceptions import (
    AuthProviderNotLinkedError,
    UserNotFoundError,
)


async def test_login_via_auth_provider_use_case_success(
    register_via_password,
    link_auth_provider,
    login_via_auth_provider,
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    await link_auth_provider.execute(user.user_id, auth_provider, auth_provider_user_id)

    access_token, refresh_token, csrf_token = await login_via_auth_provider.execute(
        auth_provider, auth_provider_user_id
    )
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert isinstance(csrf_token, str)


async def test_unlink_auth_provider_use_case_success(
    register_via_password,
    link_auth_provider,
    unlink_auth_provider,
    authenticate,
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider1 = "google"
    auth_provider_user_id1 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider1, auth_provider_user_id1
    )

    auth_provider2 = "github"
    auth_provider_user_id2 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider2, auth_provider_user_id2
    )

    auth_provider3 = "apple"
    auth_provider_user_id3 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider3, auth_provider_user_id3
    )

    await unlink_auth_provider.execute(
        user.user_id,
        auth_provider1,
    )
    await unlink_auth_provider.execute(
        user.user_id,
        auth_provider2,
    )
    await unlink_auth_provider.execute(
        user.user_id,
        auth_provider3,
    )

    with pytest.raises(AuthProviderNotLinkedError):
        await authenticate.execute(auth_provider1, auth_provider_user_id1)

    with pytest.raises(AuthProviderNotLinkedError):
        await authenticate.execute(auth_provider2, auth_provider_user_id2)

    with pytest.raises(AuthProviderNotLinkedError):
        await authenticate.execute(auth_provider3, auth_provider_user_id3)


async def test_unlink_nonexistent_auth_provider_raises(
    register_via_password, link_auth_provider, unlink_auth_provider
):
    username = "ril737"
    password = "73"
    user = (await register_via_password.execute(username, password))[0]

    auth_provider1 = "google"
    auth_provider_user_id1 = uuid4().hex
    await link_auth_provider.execute(
        user.user_id, auth_provider1, auth_provider_user_id1
    )

    auth_provider2 = "github"

    with pytest.raises(AuthProviderNotLinkedError):
        await unlink_auth_provider.execute(
            user.user_id,
            auth_provider2,
        )


async def test_unlink_auth_provider_nonexistent_user_raises(unlink_auth_provider):
    with pytest.raises(UserNotFoundError):
        await unlink_auth_provider.execute(
            uuid4(),
            "github",
        )
