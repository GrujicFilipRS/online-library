from abc import abstractmethod
from uuid import UUID

from ...domain.models import Author
from ...domain.ports.services import BaseAuthorService


class AuthorService(BaseAuthorService):
    @abstractmethod
    async def get_author_details(self, author_id: UUID) -> Author: ...

    @abstractmethod
    async def list_authors(self, offset: int, limit: int) -> list[Author]: ...

    @abstractmethod
    async def list_by_nationality(
        self, nationality: str, offset: int, limit: int
    ) -> list[Author]: ...

    @abstractmethod
    async def search_by_name(
        self, name: str, offset: int, limit: int
    ) -> list[Author]: ...

    @abstractmethod
    async def create_author(
        self, name: str, nationality: str, image_url: str | None
    ) -> None: ...

    @abstractmethod
    async def update_author(
        self,
        author_id: UUID,
        name: str | None,
        nationality: str | None,
        image_url: str | None,
    ) -> None: ...

    @abstractmethod
    async def delete_author(self, author_id: UUID) -> None: ...
