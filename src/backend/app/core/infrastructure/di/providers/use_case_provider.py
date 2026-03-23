from dishka import Provider, provide, Scope
from collections.abc import Callable

from ....application.use_cases.user.register_via_password import RegisterViaPasswordUseCase
from ...units_of_work.sqlal.sqlal_user_uow import SqlAlchemyUserUnitOfWork


class UseCaseProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def provide_register_via_password(
        self,
        user_uow_factory: Callable[[], SqlAlchemyUserUnitOfWork],
    ) -> RegisterViaPasswordUseCase:
        return RegisterViaPasswordUseCase(user_uow_factory)