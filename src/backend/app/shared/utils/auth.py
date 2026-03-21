from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
from joserfc.errors import BadSignatureError, DecodeError, ExpiredTokenError
from joserfc.jwk import OctKey
from joserfc.jwt import JWTClaimsRegistry, Token, decode, encode

from ...config import Config
from ...core.domain.exceptions import (
    BadTokenSignatureError,
    DomainError,
    InvalidCredentialsError,
    InvalidISSError,
    TokenDecodeError,
    TokenExpiredError,
)
from .logging import StructuredLogger


class AuthUtils:
    """Класс для работы с аутентификацией пользователей."""

    key = OctKey.import_key(Config.APP_SECRET_KEY)

    @staticmethod
    async def create_token(user_id: UUID) -> str:
        """Создать токен для пользователя."""
        now = datetime.now(UTC)
        exp = (now + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        iat = (now - timedelta(minutes=1)).timestamp()
        claims = {"sub": str(user_id), "exp": exp, "iss": Config.APP_NAME, "iat": iat}

        # key must be atleast 32 bytes long
        token = encode({"alg": "HS256"}, claims, AuthUtils.key)  # type: ignore

        StructuredLogger.debug(
            "auth.create_token.success",
            user_id=user_id,
            expires_at=datetime.fromtimestamp(claims["exp"]).isoformat(),  # type: ignore
        )

        return token

    @staticmethod
    async def decode_token(token: str) -> Token:
        """Декодировать токен."""
        try:
            decoded_token = decode(
                token,
                AuthUtils.key,
                ["HS256"],
            )
            claims_requests = JWTClaimsRegistry(
                exp={"essential": True, "allow_blank": False},
                iss={"essential": True, "allow_blank": False},
                sub={"essential": True, "allow_blank": False},
                iat={"essential": True, "allow_blank": False},
            )
            claims_requests.validate(decoded_token.claims)

            if decoded_token.claims.get("iss") != Config.APP_NAME:
                StructuredLogger.error(
                    "auth.decode_token.invalid_iss",
                    expected_iss=Config.APP_NAME,
                    received_iss=decoded_token.claims.get("iss"),
                )
                raise InvalidISSError("invalid token iss")

            user_id = UUID(decoded_token.claims["sub"])

            StructuredLogger.debug("auth.decode_token.success", user_id=user_id)

            return decoded_token

        except ExpiredTokenError as e:
            StructuredLogger.warning("auth.decode_token.expired")
            raise TokenExpiredError("token expired") from e

        except DecodeError as e:
            StructuredLogger.warning("auth.decode_token.decode_error", error=e)
            raise TokenDecodeError("failed to decode token") from e

        except BadSignatureError as e:
            StructuredLogger.warning("auth.decode_token.bad_signature", error=str(e))
            raise BadTokenSignatureError("bad token signature") from e

        except Exception as e:
            StructuredLogger.exception(
                "auth.decode_token.unexpected_error", error=str(e)
            )
            raise DomainError("unexpected error") from e

    @staticmethod
    async def get_user_id_from_token(token: str) -> UUID:
        """Получить информацию о пользователе из токена."""
        payload = await AuthUtils.decode_token(token)

        user_id = payload.claims.get("sub")
        if not user_id:
            StructuredLogger.warning("auth.get_user_from_token.no_user_id")
            raise TokenDecodeError("failed to get user id")

        return UUID(user_id)

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> None:
        """Проверить пароль пользователя."""

        try:
            is_valid = bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )
            StructuredLogger.debug(
                "auth.password_verification.result",
                result="success" if is_valid else "failure",
            )

        except Exception as e:
            StructuredLogger.exception(
                "auth.password_verification.unexpected_error", error=e
            )
            raise InvalidCredentialsError("invalid credentials") from e

    @staticmethod
    async def hash_password(password: str) -> str:
        """Хеширование пароля"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
