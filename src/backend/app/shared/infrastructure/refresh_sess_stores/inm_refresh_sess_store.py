from datetime import datetime, timedelta
from json import dumps, loads
from uuid import UUID

from ...domain.ports import BaseRefreshSessionStorage, RefreshSession
from ..inm_storage import InMemoryStorage


class InMemoryRefreshSessionStorage(BaseRefreshSessionStorage):
    def __init__(self, inm_storage: InMemoryStorage):
        self.inm_storage = inm_storage

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
        self.inm_storage.refresh_sessions[self._key(jwt_id)] = payload
        ex = datetime.now() + timedelta(seconds=ttl_seconds)
        self.inm_storage.refresh_sessions_ttl[self._key(jwt_id)] = ex

    async def get(self, jwt_id: UUID) -> RefreshSession | None:
        raw = self.inm_storage.refresh_sessions.get(self._key(jwt_id))
        if raw is None:
            return None
        ex = self.inm_storage.refresh_sessions_ttl.get(self._key(jwt_id))
        if ex is None:
            return None
        if datetime.now() > ex:
            await self.delete(jwt_id)
            return None
        data = loads(raw)
        return RefreshSession(
            sub=UUID(data["sub"]),
            sid=UUID(data["sid"]),
        )

    async def delete(self, jwt_id: UUID) -> None:
        del self.inm_storage.refresh_sessions[self._key(jwt_id)]
