from uuid import uuid4

from ....config import get_config
from ....shared.domain.ports import BaseRefreshSessionStorage
from ....shared.utils.auth import AuthUtils
from ...domain.exceptions import InvalidCredentialsError
from ...domain.models import User
from ...domain.ports.repositories import BaseUserRepository
from ...domain.ports.services import BaseAuthService

config = get_config()


class AuthService(BaseAuthService):
    def __init__(
        self,
        user_repo: BaseUserRepository,
        refresh_sess_store: BaseRefreshSessionStorage,
    ):
        self.user_repo = user_repo
        self.refresh_sess_store = refresh_sess_store

    async def login_user(self, user: User, password: str) -> tuple[str, str, str]:
        if not await AuthUtils.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("invalid credentials")

        sess_id = uuid4()
        jwt_id = uuid4()
        ttl_seconds = int(config.ACCESS_TTL.total_seconds())

        access_token = await AuthUtils.create_access_token(user.user_id, sess_id)
        refresh_token = await AuthUtils.create_refresh_token(
            user.user_id, sess_id, jwt_id
        )
        csrf_token = await AuthUtils.create_csrf_token(sess_id)

        await self.refresh_sess_store.create(jwt_id, user.user_id, sess_id, ttl_seconds)

        return access_token, refresh_token, csrf_token
