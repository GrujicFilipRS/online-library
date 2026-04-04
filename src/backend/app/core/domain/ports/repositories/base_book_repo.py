from abc import ABC, abstractmethod
from uuid import UUID

from ...models import Book


class BaseBookRepository(ABC):
    @abstractmethod
    async def get_by_id(self, book_id: UUID) -> Book | None: ...

    @abstractmethod
    async def save(self, book: Book) -> None: ...

    @abstractmethod
    async def delete(self, book_id: UUID) -> None: ...

    @abstractmethod
    async def list_all(self, offset: int, limit: int) -> list[Book]: ...

    @abstractmethod
    async def list_by_author(
        self, author_id: UUID, offset: int, limit: int
    ) -> list[Book]: ...

    @abstractmethod
    async def list_by_published_year(
        self, year: int, offset: int, limit: int
    ) -> list[Book]: ...

    @abstractmethod
    async def search_by_name(
        self, name: str, offset: int, limit: int
    ) -> list[Book]: ...
