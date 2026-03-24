from sqlalchemy.ext.asyncio import AsyncSession

from .....shared.infra.refresh_sess_stores import RedisRefreshSessionStorage
from .....shared.infra.units_of_work import SqlAlchemyUnitOfWork
from ....domain.ports.units_of_work import BaseUserUnitOfWork
from ...repositories.sqlal import SqlAlchemyUserRepository
from ...services import AuthService, UserService


class SqlAlchemyUserUnitOfWork(SqlAlchemyUnitOfWork, BaseUserUnitOfWork):
    def __init__(self, db_sess: AsyncSession):
        super().__init__(db_sess)
        self.user_repo = SqlAlchemyUserRepository(db_sess)
        self.user_service = UserService(self.user_repo)
        self.refresh_sess_store = RedisRefreshSessionStorage()
        self.auth_service = AuthService(self.user_repo, self.refresh_sess_store)
