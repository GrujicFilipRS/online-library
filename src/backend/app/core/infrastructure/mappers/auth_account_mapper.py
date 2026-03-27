from ...domain.models import AuthAccount
from ...domain.value_objects import AuthProvider, AuthProviderUserId
from ..db_models import DBAuthAccount
from ..dto import AuthAccountDTO


class AuthAccountMapper:
    @staticmethod
    def to_domain(db_auth_account: DBAuthAccount) -> AuthAccount:
        return AuthAccount(
            auth_account_id=db_auth_account.auth_account_id,
            user_id=db_auth_account.user_id,
            auth_provider=AuthProvider(value=db_auth_account.auth_provider),
            auth_provider_user_id=AuthProviderUserId(
                value=db_auth_account.auth_provider_user_id
            ),
            created_at=db_auth_account.created_at,
        )

    @staticmethod
    def to_orm(auth_account: AuthAccount) -> DBAuthAccount:
        return DBAuthAccount(
            auth_account_id=auth_account.auth_account_id,
            user_id=auth_account.user_id,
            auth_provider=auth_account.auth_provider.value,
            auth_provider_user_id=auth_account.auth_provider_user_id.value,
            created_at=auth_account.created_at,
        )

    @staticmethod
    def to_dto(auth_account: AuthAccount) -> AuthAccountDTO:
        return AuthAccountDTO(
            auth_account_id=auth_account.auth_account_id,
            user_id=auth_account.user_id,
            auth_provider=auth_account.auth_provider.value,
            auth_provider_user_id=auth_account.auth_provider_user_id.value,
            created_at=auth_account.created_at,
        )
