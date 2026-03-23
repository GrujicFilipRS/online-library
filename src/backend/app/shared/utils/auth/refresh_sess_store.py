from dataclasses import dataclass
from json import dumps, loads
from uuid import UUID

from .. import RedisClient


@dataclass(slots=True)
class RefreshSession:
    sub: str
    sid: str


class RefreshSessionStorage:
    @staticmethod
    def _key(jwt_id: UUID) -> str:
        return f"refresh:{jwt_id}"

    @classmethod
    async def create(
        cls,
        jwt_id: UUID,
        user_id: UUID,
        sess_id: UUID,
        ttl_seconds: int,
    ) -> None:
        payload = dumps({"sub": user_id, "sid": sess_id})
        await RedisClient.set(cls._key(jwt_id), payload, ex=ttl_seconds)

    @classmethod
    async def get(cls, jwt_id: UUID) -> RefreshSession | None:
        raw = await RedisClient.get(cls._key(jwt_id))
        if raw is None:
            return None
        data = loads(raw)
        return RefreshSession(sub=data["sub"], sid=data["sid"])

    @classmethod
    async def delete(cls, jwt_id: UUID) -> None:
        await RedisClient.delete(cls._key(jwt_id))
