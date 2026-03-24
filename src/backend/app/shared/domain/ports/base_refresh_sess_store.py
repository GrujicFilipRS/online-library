from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class RefreshSession:
    sub: UUID
    sid: UUID


class BaseRefreshSessionStorage(ABC):
    @staticmethod
    @abstractmethod
    def _key(jwt_id: UUID) -> str: ...

    @abstractmethod
    async def create(
        self,
        jwt_id: UUID,
        user_id: UUID,
        sess_id: UUID,
        ttl_seconds: int,
    ) -> None: ...

    @abstractmethod
    async def get(self, jwt_id: UUID) -> RefreshSession | None: ...

    @abstractmethod
    async def delete(self, jwt_id: UUID) -> None: ...
