from dishka import Provider, Scope, provide

from ...repositories.sqlal import SqlAlchemyUserRepository
from ...services import UserService


class ServiceProvider(Provider):
    """Провайдер для внедрения сервисов в приложение."""

    @provide(scope=Scope.REQUEST)
    async def user_service(self, user_repo: SqlAlchemyUserRepository) -> UserService:
        return UserService(user_repo)
