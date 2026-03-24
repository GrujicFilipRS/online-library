from uuid import uuid4

from src.backend.app.core.domain.models import AuthAccount, User
from src.backend.app.core.domain.value_objects import AuthProvider, AuthProviderUserId


async def test_save_inserts_new_auth_account(auth_account_repo, user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    auth_account = AuthAccount.create(
        user.user_id, auth_provider, auth_provider_user_id
    )

    await auth_account_repo.save(auth_account)

    get_auth_account = await auth_account_repo.get_by_id(auth_account.auth_account_id)

    assert isinstance(get_auth_account, AuthAccount)
    assert get_auth_account.auth_account_id == auth_account.auth_account_id
    assert get_auth_account.user_id == auth_account.user_id
    assert get_auth_account.auth_provider.value == auth_account.auth_provider.value
    assert (
        get_auth_account.auth_provider_user_id.value
        == auth_account.auth_provider_user_id.value
    )
    assert get_auth_account.created_at == auth_account.created_at


async def test_save_updates_existing_auth_account(auth_account_repo, user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    auth_account = AuthAccount.create(
        user.user_id, auth_provider, auth_provider_user_id
    )

    await auth_account_repo.save(auth_account)

    auth_provider_vo = AuthProvider("google")
    auth_provider_user_id_vo = AuthProviderUserId(uuid4().hex)

    auth_account.auth_provider = auth_provider_vo
    auth_account.auth_provider_user_id = auth_provider_user_id_vo

    await auth_account_repo.save(auth_account)

    get_auth_account = await auth_account_repo.get_by_id(auth_account.auth_account_id)

    assert get_auth_account.auth_provider.value == auth_provider_vo.value
    assert (
        get_auth_account.auth_provider_user_id.value == auth_provider_user_id_vo.value
    )


async def test_get_auth_accounts_by_user_id(auth_account_repo, user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    auth_provider1 = "google"
    auth_provider_user_id1 = uuid4().hex
    auth_account1 = AuthAccount.create(
        user.user_id, auth_provider1, auth_provider_user_id1
    )

    auth_provider2 = "github"
    auth_provider_user_id2 = uuid4().hex
    auth_account2 = AuthAccount.create(
        user.user_id, auth_provider2, auth_provider_user_id2
    )

    await auth_account_repo.save(auth_account1)
    await auth_account_repo.save(auth_account2)

    get_auth_accounts = await auth_account_repo.get_by_user_id(user.user_id)

    assert isinstance(get_auth_accounts, list)
    assert len(get_auth_accounts) == 2


async def test_get_auth_account_by_auth_provider(auth_account_repo, user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    auth_account = AuthAccount.create(
        user.user_id, auth_provider, auth_provider_user_id
    )

    await auth_account_repo.save(auth_account)

    auth_provider_vo = AuthProvider(auth_provider)
    auth_provider_user_id_vo = AuthProviderUserId(auth_provider_user_id)
    get_auth_account = await auth_account_repo.get_by_auth_provider(
        auth_provider_vo,
        auth_provider_user_id_vo,
    )

    assert isinstance(get_auth_account, AuthAccount)


async def test_get_nonexistent_auth_account_returns_none(auth_account_repo):
    assert await auth_account_repo.get_by_id(uuid4()) is None
    assert await auth_account_repo.get_by_user_id(uuid4()) == []
    assert (
        await auth_account_repo.get_by_auth_provider(
            AuthProvider("google"), AuthProviderUserId(uuid4().hex)
        )
        is None
    )


async def test_delete_auth_account(auth_account_repo, user_repo):
    username = "ril737"
    password = "73"
    user = User.create(username, password)

    await user_repo.save(user)

    auth_provider = "google"
    auth_provider_user_id = uuid4().hex
    auth_account = AuthAccount.create(
        user.user_id, auth_provider, auth_provider_user_id
    )

    await auth_account_repo.save(auth_account)

    get_auth_account = await auth_account_repo.get_by_id(auth_account.auth_account_id)

    await auth_account_repo.delete(get_auth_account.auth_account_id)

    get_auth_account = await auth_account_repo.get_by_id(auth_account.auth_account_id)

    assert get_auth_account is None
