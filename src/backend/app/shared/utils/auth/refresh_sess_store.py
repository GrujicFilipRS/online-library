from dataclasses import dataclass
from json import dumps, loads
from uuid import UUID

from .. import RedisClient


@dataclass(slots=True)
class RefreshSession:
    sub: UUID
    sid: UUID


class RefreshSessionStorage:
    @staticmethod
    def _key(jwt_id: UUID) -> str:
        return f"refresh:{jwt_id.hex}"

    @classmethod
    async def create(
        cls,
        jwt_id: UUID,
        user_id: UUID,
        sess_id: UUID,
        ttl_seconds: int,
    ) -> None:
        payload = dumps({"sub": user_id.hex, "sid": sess_id.hex})
        await RedisClient.set(cls._key(jwt_id), payload, ex=ttl_seconds)

    @classmethod
    async def get(cls, jwt_id: UUID) -> RefreshSession | None:
        raw = await RedisClient.get(cls._key(jwt_id))
        if raw is None:
            return None
        data = loads(raw)
        return RefreshSession(
            sub=UUID(data["sub"]),
            sid=UUID(data["sid"]),
        )

    @classmethod
    async def delete(cls, jwt_id: UUID) -> None:
        await RedisClient.delete(cls._key(jwt_id))
