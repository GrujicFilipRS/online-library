from collections.abc import Callable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ...units_of_work.sqlal import (
    SqlAlchemyAuthAccountUnitOfWork,
    SqlAlchemyUserUnitOfWork,
)


class UnitOfWorkFactoryProvider(Provider):
    """Provider for implementing units of work in the application"""

    @provide(scope=Scope.REQUEST)
    async def provide_user_uow_factory(
        self, db_sess: AsyncSession
    ) -> Callable[[], SqlAlchemyUserUnitOfWork]:
        return lambda: SqlAlchemyUserUnitOfWork(db_sess)

    @provide(scope=Scope.REQUEST)
    async def provide_auth_account_uow_factory(
        self, db_sess: AsyncSession
    ) -> Callable[[], SqlAlchemyAuthAccountUnitOfWork]:
        return lambda: SqlAlchemyAuthAccountUnitOfWork(db_sess)
