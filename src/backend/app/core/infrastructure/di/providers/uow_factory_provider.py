from collections.abc import Callable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ...units_of_work.sqlal import SqlAlchemyUserUnitOfWork


class UnitOfWorkFactoryProvider(Provider):
    """Provider for implementing units of work in the application"""

    @provide(scope=Scope.REQUEST)
    async def user_uow_factory(
        self,
        db_sess: AsyncSession,
    ) -> Callable[[], SqlAlchemyUserUnitOfWork]:
        return lambda: SqlAlchemyUserUnitOfWork(db_sess)
