from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from ...models import Book


class BaseBookService(ABC):
    @abstractmethod
    async def get_book_by_id(self, book_id: UUID) -> Book: ...

    @abstractmethod
    async def list_books(self, offset: int, limit: int) -> list[Book]: ...

    @abstractmethod
    async def create_boook(
        self,
        title: str,
        description: str,
        published_year: int,
        cover_image_url: str,
        author_id: UUID,
        uploaded_by: UUID,
        created: datetime,
    ) -> Book: ...

    @abstractmethod
    async def update_book(
        self,
        book_id: UUID,
        title: str,
        description: str,
        published_year: int,
        cover_image_url: str,
        author_id: UUID,
        uploaded_by: UUID,
        created: datetime,
    ) -> Book: ...

    @abstractmethod
    async def delete_book(self, book_id: UUID) -> None: ...

    @abstractmethod
    async def search_by_name(
        self, name: str, offset: int, limit: int
    ) -> list[Book]: ...

    @abstractmethod
    async def list_by_author(
        self, author_id: UUID, offset: int, limit: int
    ) -> list[Book]: ...

    @abstractmethod
    async def list_by_published_year(
        self, year: int, offset: int, limit: int
    ) -> list[Book]: ...
