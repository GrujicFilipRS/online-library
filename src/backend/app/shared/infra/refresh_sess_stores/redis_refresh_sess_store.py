from json import dumps, loads
from uuid import UUID

from ...domain.ports import BaseRefreshSessionStorage, RefreshSession
from ...utils import RedisClient


class RedisRefreshSessionStorage(BaseRefreshSessionStorage):
    @staticmethod
    def _key(jwt_id: UUID) -> str:
        return f"refresh:{jwt_id.hex}"

    async def create(
        self,
        jwt_id: UUID,
        user_id: UUID,
        sess_id: UUID,
        ttl_seconds: int,
    ) -> None:
        payload = dumps({"sub": user_id.hex, "sid": sess_id.hex})
        await RedisClient.set(self._key(jwt_id), payload, ex=ttl_seconds)

    async def get(self, jwt_id: UUID) -> RefreshSession | None:
        raw = await RedisClient.get(self._key(jwt_id))
        if raw is None:
            return None
        data = loads(raw)
        return RefreshSession(
            sub=UUID(data["sub"]),
            sid=UUID(data["sid"]),
        )

    async def delete(self, jwt_id: UUID) -> None:
        await RedisClient.delete(self._key(jwt_id))
