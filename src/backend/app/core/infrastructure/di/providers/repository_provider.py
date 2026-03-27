from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.sqlal import (
    SqlAlchemyAuthAccountRepository,
    SqlAlchemyUserRepository,
)


class RepositoryProvider(Provider):
    """Provider for embedding repositories in the application."""

    @provide(scope=Scope.REQUEST)
    async def provide_user_repo(
        self, db_sess: AsyncSession
    ) -> SqlAlchemyUserRepository:
        return SqlAlchemyUserRepository(db_sess)

    @provide(scope=Scope.REQUEST)
    async def provide_auth_account_repo(
        self, db_sess: AsyncSession
    ) -> SqlAlchemyAuthAccountRepository:
        return SqlAlchemyAuthAccountRepository(db_sess)
