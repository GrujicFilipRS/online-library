from uuid import UUID

from .....shared.infra.units_of_work import InMemoryStorage
from ....domain.models import Author
from ....domain.ports.repositories import BaseAuthorRepository


class InMemoryAuthorRepository(BaseAuthorRepository):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

    async def get_by_id(self, author_id: UUID) -> Author | None:
        return next(
            (a for a in self.inm_storage.authors if a.author_id == author_id), None
        )

    async def list_all(self, offset: int, limit: int) -> list[Author]:
        authors = self.inm_storage.authors
        return authors[offset : offset + limit]

    async def search_by_name(self, name: str, offset: int, limit: int) -> list[Author]:
        authors = self.inm_storage.authors
        authors_with_searched_name = [
            a for a in authors if name.lower() in a.name.lower()
        ]
        return authors_with_searched_name[offset : offset + limit]

    async def get_by_nationality(
        self, nationality: str, offset: int, limit: int
    ) -> list[Author]:
        authors = [a for a in self.inm_storage.authors if a.nationality == nationality]
        return authors[offset : offset + limit]

    async def save(self, author: Author) -> None:
        await self.delete(author.author_id)
        self.inm_storage.authors.append(author)

    async def delete(self, author_id: UUID) -> None:
        self.inm_storage.authors = [
            a for a in self.inm_storage.authors if a.author_id != author_id
        ]
