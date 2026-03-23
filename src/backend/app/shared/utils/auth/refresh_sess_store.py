from dataclasses import dataclass
from json import dumps, loads
from uuid import UUID

from .. import RedisClient


@dataclass(slots=True)
class RefreshSession:
    sub: str
    sid: str


class RefreshSessionStorage:
    def __init__(self, redis_client: RedisClient) -> None:
        self._redis_client = redis_client

    @staticmethod
    def _key(jwt_id: UUID) -> str:
        return f"refresh:{jwt_id}"

    async def create(
        self, jwt_id: UUID, user_id: UUID, sess_id: UUID, ttl_seconds: int
    ) -> None:
        payload = dumps({"sub": user_id, "sid": sess_id})
        await self._redis_client.set(self._key(jwt_id), payload, ex=ttl_seconds)

    async def get(self, jwt_id: UUID) -> RefreshSession | None:
        raw = await self._redis_client.get(self._key(jwt_id))
        if raw is None:
            return None
        data = loads(raw)
        return RefreshSession(sub=data["sub"], sid=data["sid"])

    async def delete(self, jwt_id: UUID) -> None:
        await self._redis_client.delete(self._key(jwt_id))
