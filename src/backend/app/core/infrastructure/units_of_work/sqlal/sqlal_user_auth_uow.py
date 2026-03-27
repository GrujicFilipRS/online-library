from sqlalchemy.ext.asyncio import AsyncSession

from .....shared.infrastructure.refresh_sess_stores import RedisRefreshSessionStorage
from .....shared.infrastructure.units_of_work import SqlAlchemyUnitOfWork
from ....domain.ports.units_of_work import BaseUserAuthUnitOfWork
from ...repositories.sqlal import (
    SqlAlchemyAuthAccountRepository,
    SqlAlchemyUserRepository,
)
from ...services import AuthAccountService, AuthService, UserService


class SqlAlchemyUserAuthUnitOfWork(SqlAlchemyUnitOfWork, BaseUserAuthUnitOfWork):
    def __init__(self, db_sess: AsyncSession):
        super().__init__(db_sess)
        self.user_repo = SqlAlchemyUserRepository(db_sess)
        self.user_service = UserService(self.user_repo)
        self.refresh_sess_store = RedisRefreshSessionStorage()
        self.auth_service = AuthService(self.user_repo, self.refresh_sess_store)
        self.auth_account_repo = SqlAlchemyAuthAccountRepository(db_sess)
        self.auth_account_service = AuthAccountService(self.auth_account_repo)
