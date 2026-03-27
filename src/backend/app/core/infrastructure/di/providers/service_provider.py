from dishka import Provider, Scope, provide

from .....shared.infrastructure.refresh_sess_stores import RedisRefreshSessionStorage
from ...repositories.sqlal import (
    SqlAlchemyAuthAccountRepository,
    SqlAlchemyUserRepository,
)
from ...services import AuthAccountService, AuthService, UserService


class ServiceProvider(Provider):
    """Provider for implementing services in the application."""

    @provide(scope=Scope.REQUEST)
    async def provide_user_service(
        self, user_repo: SqlAlchemyUserRepository
    ) -> UserService:
        return UserService(user_repo)

    @provide(scope=Scope.REQUEST)
    async def provide_refresh_sess_store(self) -> RedisRefreshSessionStorage:
        return RedisRefreshSessionStorage()

    @provide(scope=Scope.REQUEST)
    async def provide_auth_service(
        self,
        user_repo: SqlAlchemyUserRepository,
        refresh_sess_store: RedisRefreshSessionStorage,
    ) -> AuthService:
        return AuthService(user_repo, refresh_sess_store)

    @provide(scope=Scope.REQUEST)
    async def provide_auth_account_service(
        self, auth_account_repo: SqlAlchemyAuthAccountRepository
    ) -> AuthAccountService:
        return AuthAccountService(auth_account_repo)
