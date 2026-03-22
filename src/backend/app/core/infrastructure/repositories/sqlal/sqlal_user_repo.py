from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import User
from ....domain.ports.repositories import BaseUserRepository
from ...db_models import DBUser
from ...mappers import UserMapper


class SqlAlchemyUserRepository(BaseUserRepository):
    def __init__(self, db_sess: AsyncSession):
        self.db_sess = db_sess

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = await self.db_sess.execute(
            select(DBUser).where(DBUser.user_id == user_id)
        )
        db_user = query.scalar_one_or_none()
        if db_user is None:
            return None
        user = UserMapper.to_domain(db_user)
        return user

    async def get_by_username(self, username: str) -> User | None:
        query = await self.db_sess.execute(
            select(DBUser).where(DBUser.username == username)
        )
        db_user = query.scalar_one_or_none()
        if db_user is None:
            return None
        user = UserMapper.to_domain(db_user)
        return user

    async def save(self, user: User) -> None:
        query = await self.db_sess.execute(
            select(DBUser).where(DBUser.user_id == user.user_id)
        )
        result = query.scalar_one_or_none()

        if result is None:
            db_user = UserMapper.to_orm(user)
            self.db_sess.add(db_user)
            await self.db_sess.flush()
            return

        query = await self.db_sess.execute(
            update(DBUser)
            .where(DBUser.user_id == user.user_id)
            .values(
                username=user.username.value,
                hashed_password=user.hashed_password,
                role=user.role.value,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.db_sess.flush()

    async def delete(self, user: User) -> None:
        await self.db_sess.execute(delete(DBUser).where(DBUser.user_id == user.user_id))
        await self.db_sess.flush()
