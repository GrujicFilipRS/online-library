from datetime import datetime
from uuid import UUID, uuid4

from src.backend.app.core.domain.models import AuthAccount
from src.backend.app.core.domain.value_objects import AuthProvider, AuthProviderUserId


async def test_auth_account_create_success():
    user_id = uuid4()
    auth_provider = "google"
    auth_provider_user_id = uuid4().hex

    auth_account = AuthAccount.create(user_id, auth_provider, auth_provider_user_id)

    assert isinstance(auth_account.auth_account_id, UUID)
    assert isinstance(auth_account.user_id, UUID)
    assert isinstance(auth_account.auth_provider, AuthProvider)
    assert auth_account.auth_provider.value == auth_provider
    assert isinstance(auth_account.auth_provider_user_id, AuthProviderUserId)
    assert auth_account.auth_provider_user_id.value == auth_provider_user_id
    assert isinstance(auth_account.created_at, datetime)
