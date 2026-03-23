from uuid import uuid4

from ....config import get_config
from ....shared.utils.auth import AuthUtils, RefreshSessionStorage
from ...domain.exceptions import InvalidCredentialsError
from ...domain.models import User
from ...domain.ports.repositories import BaseUserRepository
from ...domain.ports.services import BaseAuthService

config = get_config()


class AuthService(BaseAuthService):
    def __init__(self, user_repo: BaseUserRepository):
        self.user_repo = user_repo

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

        await RefreshSessionStorage.create(jwt_id, user.user_id, sess_id, ttl_seconds)

        return access_token, refresh_token, csrf_token
