from uuid import uuid4

import pytest

from src.backend.app.core.domain.exceptions import (
    AuthProviderAccountAlreadyInUseError,
    AuthProviderNotLinkedError,
    UserNotFoundError,
)
from src.backend.app.core.infrastructure.services import AuthAccountService, UserService


@pytest.fixture
async def auth_account_service(auth_account_repo):
    return AuthAccountService(auth_account_repo)


@pytest.fixture
async def user_service(user_repo):
    return UserService(user_repo)


async def test_link_auth_providers_to_user_and_authenticate_successfully(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider1 = "google"
    auth_provider2 = "github"
    auth_provider3 = "apple"
    auth_provider_user_id = uuid4().hex

    auth_account1 = await auth_account_service.link_auth_provider_to_user(
        user.user_id,
        auth_provider1,
        auth_provider_user_id,
    )
    auth_account2 = await auth_account_service.link_auth_provider_to_user(
        user.user_id,
        auth_provider2,
        auth_provider_user_id,
    )
    auth_account3 = await auth_account_service.link_auth_provider_to_user(
        user.user_id,
        auth_provider3,
        auth_provider_user_id,
    )

    get_auth_account1 = await auth_account_service.authenticate_via_auth_provider(
        auth_provider1,
        auth_provider_user_id,
    )
    get_auth_account2 = await auth_account_service.authenticate_via_auth_provider(
        auth_provider2,
        auth_provider_user_id,
    )
    get_auth_account3 = await auth_account_service.authenticate_via_auth_provider(
        auth_provider3,
        auth_provider_user_id,
    )

    assert get_auth_account1.auth_account_id == auth_account1.auth_account_id
    assert get_auth_account2.auth_account_id == auth_account2.auth_account_id
    assert get_auth_account3.auth_account_id == auth_account3.auth_account_id


async def test_link_auth_provider_to_user_duplicate_raises(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider, auth_provider_user_id
    )

    with pytest.raises(AuthProviderAccountAlreadyInUseError):
        await auth_account_service.link_auth_provider_to_user(
            user.user_id, auth_provider, auth_provider_user_id
        )


async def test_authenticate_nonexistent_auth_provider_raises(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider = "github"
    auth_provider_user_id = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider, auth_provider_user_id
    )

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.authenticate_via_auth_provider(
            "google", auth_provider_user_id
        )


async def test_link_and_unlink_auth_providers_successfully(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider1 = "google"
    auth_provider2 = "github"
    auth_provider3 = "apple"
    auth_provider_user_id = uuid4().hex

    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider1, auth_provider_user_id
    )
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider2, auth_provider_user_id
    )
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider3, auth_provider_user_id
    )

    await auth_account_service.unlink_auth_provider_from_user(
        user.user_id,
        auth_provider1,
        True,
    )
    await auth_account_service.unlink_auth_provider_from_user(
        user.user_id,
        auth_provider2,
        True,
    )
    await auth_account_service.unlink_auth_provider_from_user(
        user.user_id,
        auth_provider3,
        True,
    )

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.authenticate_via_auth_provider(
            auth_provider1, auth_provider_user_id
        )

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.authenticate_via_auth_provider(
            auth_provider2, auth_provider_user_id
        )

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.authenticate_via_auth_provider(
            auth_provider3, auth_provider_user_id
        )


async def test_unlink_nonexistent_auth_provider_raises(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider1 = "github"
    auth_provider_user_id = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider1, auth_provider_user_id
    )

    auth_provider2 = "googl"

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.unlink_auth_provider_from_user(
            user.user_id,
            auth_provider2,
            True,
        )


async def test_unlink_auth_provider_nonexistent_user_raises(auth_account_service):
    with pytest.raises(UserNotFoundError):
        await auth_account_service.unlink_auth_provider_from_user(
            uuid4(),
            "github",
            True,
        )


async def test_list_user_auth_providers_successfully(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider1 = "google"
    auth_provider2 = "github"
    auth_provider3 = "apple"
    auth_provider_user_id = uuid4().hex

    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider1, auth_provider_user_id
    )
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider2, auth_provider_user_id
    )
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider3, auth_provider_user_id
    )

    auth_providers = await auth_account_service.list_user_auth_providers(user.user_id)
    assert isinstance(auth_providers, list)
    assert len(auth_providers) == 3


async def test_change_auth_provider_identifier_successfully(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider = "github"
    auth_provider_user_id1 = uuid4().hex
    auth_account = await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider, auth_provider_user_id1
    )

    auth_provider_user_id2 = uuid4().hex

    await auth_account_service.change_auth_provider_identifier(
        user.user_id, auth_provider, auth_provider_user_id2
    )

    get_auth_account = await auth_account_service.authenticate_via_auth_provider(
        auth_provider,
        auth_provider_user_id2,
    )

    assert get_auth_account.auth_account_id == auth_account.auth_account_id


async def test_change_auth_provider_identifier_duplicate_raises(
    auth_account_service, user_service
):
    username1 = "ril737"
    password1 = "73"
    user1 = await user_service.create_user(username1, password1)

    auth_provider = "github"
    auth_provider_user_id = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user1.user_id, auth_provider, auth_provider_user_id
    )

    username2 = "ril373"
    password2 = "37"
    user2 = await user_service.create_user(username2, password2)

    with pytest.raises(AuthProviderAccountAlreadyInUseError):
        await auth_account_service.change_auth_provider_identifier(
            user2.user_id, auth_provider, auth_provider_user_id
        )


async def test_change_nonexistent_auth_provider_identifier_raises(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider1 = "github"
    auth_provider_user_id1 = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider1, auth_provider_user_id1
    )

    auth_provider2 = "google"
    auth_provider_user_id2 = uuid4().hex

    with pytest.raises(AuthProviderNotLinkedError):
        await auth_account_service.change_auth_provider_identifier(
            user.user_id, auth_provider2, auth_provider_user_id2
        )


async def test_change_auth_provider_identifier_nonexistent_user_raises(
    auth_account_service, user_service
):
    username = "ril737"
    password = "73"
    user = await user_service.create_user(username, password)

    auth_provider = "github"
    auth_provider_user_id1 = uuid4().hex
    await auth_account_service.link_auth_provider_to_user(
        user.user_id, auth_provider, auth_provider_user_id1
    )

    auth_provider_user_id2 = uuid4().hex

    with pytest.raises(UserNotFoundError):
        await auth_account_service.change_auth_provider_identifier(
            uuid4(), auth_provider, auth_provider_user_id2
        )
