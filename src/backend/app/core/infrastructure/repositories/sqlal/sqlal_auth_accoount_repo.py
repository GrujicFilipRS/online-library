from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import AuthAccount
from ....domain.ports.repositories import BaseAuthAccountRepository
from ....domain.value_objects import Provider, ProviderUserId
from ...db_models import DBAuthAccount
from ...mappers import AuthAccountMapper


class SqlAlchemyAuthAccountRepository(BaseAuthAccountRepository):
    def __init__(self, db_sess: AsyncSession):
        self.db_sess = db_sess

    async def get_by_id(self, account_id: UUID) -> AuthAccount | None:
        query = await self.db_sess.execute(
            select(DBAuthAccount).where(DBAuthAccount.id == account_id)
        )
        db_auth_account = query.scalar_one_or_none()
        if db_auth_account is None:
            return None
        auth_account = AuthAccountMapper.to_domain(db_auth_account)
        return auth_account

    async def get_by_user_id(self, user_id: UUID) -> list[AuthAccount]:
        query = await self.db_sess.execute(
            select(DBAuthAccount).where(DBAuthAccount.user_id == user_id)
        )
        db_auth_accounts = query.scalars().all()
        auth_accounts = []
        for db_acc in db_auth_accounts:
            auth_accounts.append(AuthAccountMapper.to_domain(db_acc))
        return auth_accounts

    async def get_by_provider(
        self, provider: Provider, provider_user_id: ProviderUserId
    ) -> AuthAccount | None:
        query = await self.db_sess.execute(
            select(DBAuthAccount).where(
                DBAuthAccount.provider == provider.value,
                DBAuthAccount.provider_user_id == provider_user_id.value,
            )
        )
        db_auth_account = query.scalar_one_or_none()
        if db_auth_account is None:
            return None
        auth_account = AuthAccountMapper.to_domain(db_auth_account)
        return auth_account

    async def save(self, auth_account: AuthAccount) -> None:
        query = await self.db_sess.execute(
            select(DBAuthAccount).where(DBAuthAccount.id == auth_account.id)
        )
        db_auth_account = query.scalar_one_or_none()
        if db_auth_account:
            AuthAccountMapper.update_orm(auth_account, db_auth_account)
        else:
            new_db_auth_account = AuthAccountMapper.to_orm(auth_account)
            self.db_sess.add(new_db_auth_account)
        await self.db_sess.flush()

    async def delete(self, account_id: UUID) -> None:
        await self.db_sess.execute(
            delete(DBAuthAccount).where(DBAuthAccount.id == account_id)
        )
        await self.db_sess.flush()
