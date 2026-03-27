from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Author
from ....domain.ports.repositories import BaseAuthorRepository
from ...db_models import DBAuthor
from ...mappers import AuthorMapper


class SqlAlchemyAuthorRepository(BaseAuthorRepository):
    def __init__(self, db_sess: AsyncSession):
        self.db_sess = db_sess

    async def get_by_id(self, author_id: UUID) -> Author | None:
        query = await self.db_sess.execute(
            select(DBAuthor).where(DBAuthor.author_id == author_id)
        )
        db_author = query.scalar_one_or_none()
        if not db_author:
            return None
        return AuthorMapper.to_domain(db_author)

    async def list_all(self, offset: int, limit: int) -> list[Author]:
        query = await self.db_sess.execute(select(DBAuthor).offset(offset).limit(limit))
        authors = query.scalars().all()
        return [AuthorMapper.to_domain(a) for a in authors]

    async def search_by_name(self, name: str, offset: int, limit: int) -> list[Author]:
        query = await self.db_sess.execute(
            select(DBAuthor)
            .filter(DBAuthor.name.like(f"%{name}%"))
            .offset(offset)
            .limit(limit)
        )
        authors = query.scalars().all()
        return [AuthorMapper.to_domain(a) for a in authors]

    async def get_by_nationality(
        self, nationality: str, offset: int, limit: int
    ) -> list[Author]:
        query = await self.db_sess.execute(
            select(DBAuthor)
            .filter(DBAuthor.nationality.like(f"%{nationality}%"))
            .offset(offset)
            .limit(limit)
        )
        authors = query.scalars().all()
        return [AuthorMapper.to_domain(a) for a in authors]

    async def save(self, author: Author) -> None:
        query = await self.db_sess.execute(
            select(DBAuthor).where(DBAuthor.author_id == author.author_id)
        )
        existing_author = query.scalar_one_or_none()
        if not existing_author:
            db_author = AuthorMapper.to_orm(author)
            self.db_sess.add(db_author)
            await self.db_sess.flush()
            return
        await self.db_sess.execute(
            update(DBAuthor)
            .where(DBAuthor.author_id == author.author_id)
            .values(
                name=author.name,
                nationality=author.nationality,
                image_url=author.image_url,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.db_sess.flush()

    async def delete(self, author_id: UUID) -> None:
        await self.db_sess.execute(
            delete(DBAuthor).where(DBAuthor.author_id == author_id)
        )
        await self.db_sess.flush()
