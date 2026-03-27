from abc import ABC, abstractmethod
from uuid import UUID

from ...models import Author


class BaseAuthorRepository(ABC):
    @abstractmethod
    async def get_by_id(self, author_id: UUID) -> Author | None: ...

    @abstractmethod
    async def list_all(self, offset: int, limit: int) -> list[Author]: ...

    @abstractmethod
    async def search_by_name(
        self, name: str, offset: int, limit: int
    ) -> list[Author]: ...

    @abstractmethod
    async def get_by_nationality(
        self, nationality: str, offset: int, limit: int
    ) -> list[Author]: ...

    @abstractmethod
    async def save(self, author: Author) -> None: ...

    @abstractmethod
    async def delete(self, author_id: UUID) -> None: ...
