from ...domain.models import AuthAccount
from ...domain.value_objects import Provider, ProviderUserId
from ..db_models import DBAuthAccount
from ..dto import AuthAccountDTO


class AuthAccountMapper:
    @staticmethod
    def to_domain(db_auth_account: DBAuthAccount) -> AuthAccount:
        return AuthAccount(
            account_id=db_auth_account.id,
            user_id=db_auth_account.user_id,
            provider=Provider(value=db_auth_account.provider),
            provider_user_id=ProviderUserId(value=db_auth_account.provider_user_id),
            created_at=db_auth_account.created_at,
        )

    @staticmethod
    def to_orm(auth_account: AuthAccount) -> DBAuthAccount:
        return DBAuthAccount(
            id=auth_account.id,
            user_id=auth_account.user_id,
            provider=auth_account.provider.value,
            provider_user_id=auth_account.provider_user_id.value,
            created_at=auth_account.created_at,
        )

    @staticmethod
    def update_orm(
        auth_account: AuthAccount, db_auth_account: DBAuthAccount
    ) -> DBAuthAccount:
        """explicict way to make sqlalchemy use UPDATE and avoid primary key conflicts"""
        db_auth_account.provider = auth_account.provider.value
        db_auth_account.provider_user_id = auth_account.provider_user_id.value
        return db_auth_account

    @staticmethod
    def to_dto(auth_account: AuthAccount) -> AuthAccountDTO:
        return AuthAccountDTO(
            id=auth_account.id,
            user_id=auth_account.user_id,
            provider=auth_account.provider.value,
            provider_user_id=auth_account.provider_user_id.value,
            created_at=auth_account.created_at,
        )
