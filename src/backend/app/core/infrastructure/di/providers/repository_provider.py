from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.sqlal import SqlAlchemyUserRepository


class RepositoryProvider(Provider):
    """Provider for embedding repositories in the application."""

    @provide(scope=Scope.REQUEST)
    async def user_repo(self, db_sess: AsyncSession) -> SqlAlchemyUserRepository:
        return SqlAlchemyUserRepository(db_sess)
