from uuid import UUID

from ...domain.exceptions import (
    AuthorAlreadyExistsError,
    AuthorNotFoundError,
)
from ...domain.models import Author
from ...domain.ports.repositories import BaseAuthorRepository
from ...domain.ports.services import BaseAuthorService
from ...domain.value_objects import AuthorName, ImageURL


class AuthorService(BaseAuthorService):
    def __init__(self, author_repo: BaseAuthorRepository):
        self.author_repo = author_repo

    async def get_author_details(self, author_id: UUID) -> Author:
        author = await self.author_repo.get_by_id(author_id)
        if not author:
            raise AuthorNotFoundError()
        return author

    async def list_authors(self, offset: int, limit: int) -> list[Author]:
        authors = await self.author_repo.list_all(offset, limit)
        return authors

    async def list_by_nationality(
        self, nationality: str, offset: int, limit: int
    ) -> list[Author]:
        authors = await self.author_repo.get_by_nationality(nationality, offset, limit)
        return authors

    async def search_by_name(self, name: str, offset: int, limit: int) -> list[Author]:
        authors = await self.author_repo.search_by_name(name, offset, limit)
        return authors

    async def create_author(self, name: str, nationality: str, image_url: str | None):
        existing_authors = await self.author_repo.search_by_name(
            name=name, offset=0, limit=1
        )
        if existing_authors and existing_authors[0].name.value.lower() == name.lower():
            raise AuthorAlreadyExistsError()

        author = Author.create(name=name, nationality=nationality, image_url=image_url)
        await self.author_repo.save(author)

    async def update_author(
        self,
        author_id: UUID,
        name: str | None,
        nationality: str | None,
        image_url: str | None,
    ) -> None:
        existing_author = await self.author_repo.get_by_id(author_id)
        if not existing_author:
            raise AuthorNotFoundError()
        author = Author(
            author_id=author_id,
            name=AuthorName(value=(name or existing_author.name.value)),
            nationality=nationality or existing_author.nationality,
            image_url=ImageURL(value=(image_url or existing_author.image_url.value)),
        )
        await self.author_repo.save(author)

    async def delete_author(self, author_id: UUID):
        existing_author = await self.author_repo.get_by_id(author_id)
        if not existing_author:
            raise AuthorNotFoundError()
        await self.author_repo.delete(author_id)
