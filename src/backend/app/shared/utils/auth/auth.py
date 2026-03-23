from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from hmac import new
from secrets import compare_digest, token_bytes
from uuid import UUID

from bcrypt import checkpw, gensalt, hashpw
from joserfc.jwk import OctKey
from joserfc.jwt import JWTClaimsRegistry, Token, decode, encode

from ....config import get_config
from .. import StructuredLogger

config = get_config()


class AuthUtils:
    """Class for working with the authentication of users"""

    _key = OctKey.import_key(config.APP_SECRET_KEY.get_secret_value())

    @staticmethod
    def _now_ts() -> int:
        return int(datetime.now(UTC).timestamp())

    @staticmethod
    def _b64url(data: bytes) -> str:
        return urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    @classmethod
    async def hash_password(cls, password: str) -> str:
        """Password hashing"""
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    @classmethod
    async def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verifies users password"""
        is_valid = checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
        StructuredLogger.debug(
            "auth.password_verification.result",
            result="success" if is_valid else "failure",
        )
        return is_valid

    @classmethod
    async def create_access_token(cls, user_id: UUID, sess_id: UUID) -> str:
        """Returns the access token for the user"""
        iat = cls._now_ts()
        exp = iat + int(config.ACCESS_TTL.total_seconds())
        claims = {
            "sub": str(user_id),
            "type": "access",
            "sid": str(sess_id),
            "iss": config.APP_NAME,
            "iat": iat,
            "exp": exp,
        }

        # key must be atleast 32 bytes long
        token = encode({"alg": config.ALGORITHM}, claims, cls._key)

        StructuredLogger.debug(
            "auth.create_token.success",
            user_id=user_id,
            expires_at=datetime.fromtimestamp(exp).isoformat(),
        )

        return token

    @classmethod
    async def create_refresh_token(
        cls, user_id: UUID, sess_id: UUID, jwt_id: UUID
    ) -> str:
        """Returns the refresh token for the user"""
        iat = cls._now_ts()
        exp = iat + int(config.REFRESH_TTL.total_seconds())
        claims = {
            "sub": str(user_id),
            "type": "refresh",
            "sid": str(sess_id),
            "jti": str(jwt_id),
            "iss": config.APP_NAME,
            "iat": iat,
            "exp": exp,
        }

        # key must be atleast 32 bytes long
        token = encode({"alg": config.ALGORITHM}, claims, cls._key)

        StructuredLogger.debug(
            "auth.create_token.success",
            user_id=user_id,
            expires_at=datetime.fromtimestamp(exp).isoformat(),
        )

        return token

    @classmethod
    async def decode_token(cls, token: str) -> Token | None:
        """Decodes and returns the Token"""
        decoded_token = decode(
            token,
            cls._key,
            algorithms=[config.ALGORITHM],
        )
        claims_requests = JWTClaimsRegistry(
            sub={"essential": True, "allow_blank": False},
            type={
                "essential": True,
                "allow_blank": False,
                "values": ["access", "refresh"],
            },
            sid={"essential": True, "allow_blank": False},
            iss={"essential": True, "allow_blank": False},
            iat={"essential": True, "allow_blank": False},
            exp={"essential": True, "allow_blank": False},
        )
        claims_requests.validate(decoded_token.claims)

        if decoded_token.claims.get("iss") != config.APP_NAME:
            StructuredLogger.error(
                "auth.decode_token.invalid_iss",
                expected_iss=config.APP_NAME,
                received_iss=decoded_token.claims.get("iss"),
            )
            return None

        user_id = UUID(decoded_token.claims["sub"])

        StructuredLogger.debug("auth.decode_token.success", user_id=user_id)

        return decoded_token

    @staticmethod
    async def get_user_id_from_token(token: str) -> UUID | None:
        """Gets user id from token"""
        payload = await AuthUtils.decode_token(token)
        if payload is None:
            StructuredLogger.warning("auth.get_user_from_token.no_payload")
            return None

        user_id = payload.claims.get("sub")
        if user_id is None:
            StructuredLogger.warning("auth.get_user_from_token.no_user_id")
            return None

        return UUID(user_id)

    @classmethod
    async def _sign_csrf(cls, sess_id: str, nonce: str) -> str:
        msg = f"{sess_id}.{nonce}".encode()
        sig = new(
            config.APP_CSRF_SECRET.get_secret_value().encode("utf-8"), msg, "sha256"
        ).digest()
        csrf = f"{nonce}.{cls._b64url(sig)}"
        StructuredLogger.debug(
            "auth.sign_csrf.success",
            sess_id=sess_id,
        )
        return csrf

    @classmethod
    async def create_csrf_token(cls, sess_id: str) -> str:
        nonce = cls._b64url(token_bytes(32))
        return await cls._sign_csrf(sess_id, nonce)

    @classmethod
    async def verify_csrf_token(cls, sess_id: str, token: str) -> bool:
        try:
            nonce, _sig = token.split(".", 1)
        except ValueError as e:
            StructuredLogger.exception("auth.verify_csrf_token.error", error=str(e))
            return False

        expected = await cls._sign_csrf(sess_id, nonce)
        is_valid = compare_digest(expected, token)

        StructuredLogger.debug(
            "auth.verify_csrf_token.result",
            result="success" if is_valid else "failure",
        )
        return is_valid
