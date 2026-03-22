from sqlalchemy.ext.asyncio import AsyncSession

from .....shared.infra.units_of_work import SqlAlchemyUnitOfWork
from ....domain.ports.units_of_work import BaseAuthAccountUnitOfWork
from ...repositories.sqlal import SqlAlchemyAuthAccountRepository
from ...services import AuthAccountService


class SqlAlchemyAuthAccountUnitOfWork(SqlAlchemyUnitOfWork, BaseAuthAccountUnitOfWork):
    def __init__(self, db_sess: AsyncSession):
        super().__init__(db_sess)
        self.auth_account_repo = SqlAlchemyAuthAccountRepository(self.db_sess)
        self.auth_account_service = AuthAccountService(self.auth_account_repo)
