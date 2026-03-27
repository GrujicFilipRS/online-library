from collections.abc import Callable

from dishka import Provider, Scope, provide

from ....application.use_cases.auth_account import (
    AutheticateUseCase,
    ChangeAuthProviderIdentifierUseCase,
    LinkAuthProviderUseCase,
    ListAuthProvidersUseCase,
)
from ....application.use_cases.user import (
    LoginViaPasswordUseCase,
    RegisterViaPasswordUseCase,
)
from ....application.use_cases.user_auth import UnlinkAuthProviderUseCase
from ...units_of_work.sqlal import (
    SqlAlchemyAuthAccountUnitOfWork,
    SqlAlchemyUserAuthUnitOfWork,
    SqlAlchemyUserUnitOfWork,
)


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_register_via_password(
        self,
        user_uow_factory: Callable[[], SqlAlchemyUserUnitOfWork],
    ) -> RegisterViaPasswordUseCase:
        return RegisterViaPasswordUseCase(user_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_login_via_password(
        self,
        user_uow_factory: Callable[[], SqlAlchemyUserUnitOfWork],
    ) -> LoginViaPasswordUseCase:
        return LoginViaPasswordUseCase(user_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_authenticate(
        self, auth_account_uow_factory: Callable[[], SqlAlchemyAuthAccountUnitOfWork]
    ) -> AutheticateUseCase:
        return AutheticateUseCase(auth_account_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_change_auth_provider_identifier(
        self, auth_account_uow_factory: Callable[[], SqlAlchemyAuthAccountUnitOfWork]
    ) -> ChangeAuthProviderIdentifierUseCase:
        return ChangeAuthProviderIdentifierUseCase(auth_account_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_link_auth_provider(
        self, auth_account_uow_factory: Callable[[], SqlAlchemyAuthAccountUnitOfWork]
    ) -> LinkAuthProviderUseCase:
        return LinkAuthProviderUseCase(auth_account_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_list_auth_providers(
        self, auth_account_uow_factory: Callable[[], SqlAlchemyAuthAccountUnitOfWork]
    ) -> ListAuthProvidersUseCase:
        return ListAuthProvidersUseCase(auth_account_uow_factory)

    @provide(scope=Scope.REQUEST)
    async def provide_unlink_auth_provider(
        self, user_auth_uow_factory: Callable[[], SqlAlchemyUserAuthUnitOfWork]
    ) -> UnlinkAuthProviderUseCase:
        return UnlinkAuthProviderUseCase(user_auth_uow_factory)
