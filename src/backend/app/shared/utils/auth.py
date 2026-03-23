from datetime import UTC, datetime, timedelta
from uuid import UUID

import argon2
from joserfc.errors import BadSignatureError, DecodeError, ExpiredTokenError
from joserfc.jwk import OctKey
from joserfc.jwt import JWTClaimsRegistry, Token, decode, encode

from ...config import get_config
from ...core.domain.exceptions import (
    BadTokenSignatureError,
    DomainError,
    InvalidCredentialsError,
    InvalidISSError,
    TokenDecodeError,
    TokenExpiredError,
)
from .logging import StructuredLogger

config = get_config()


class AuthUtils:
    """Class for working with the authentication of users"""

    key = OctKey.import_key(config.APP_SECRET_KEY.get_secret_value())

    @staticmethod
    async def create_token(user_id: UUID) -> str:
        """Returns the token for the user"""
        now = datetime.now(UTC)
        exp = (now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        iat = (now - timedelta(minutes=1)).timestamp()
        claims = {"sub": str(user_id), "exp": exp, "iss": config.APP_NAME, "iat": iat}

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
        """Decodes and returns the Token"""
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

            if decoded_token.claims.get("iss") != config.APP_NAME:
                StructuredLogger.error(
                    "auth.decode_token.invalid_iss",
                    expected_iss=config.APP_NAME,
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
        """Gets user id from token"""
        payload = await AuthUtils.decode_token(token)

        user_id = payload.claims.get("sub")
        if not user_id:
            StructuredLogger.warning("auth.get_user_from_token.no_user_id")
            raise TokenDecodeError("failed to get user id")

        return UUID(user_id)

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> None:
        """Verifies users password"""

        try:
            hasher = argon2.PasswordHasher()
            hasher.verify(hashed_password, password)

        except argon2.exceptions.VerifyMismatchError as err:
            raise InvalidCredentialsError("invalid credentials") from err

        except Exception as e:
            StructuredLogger.exception(
                "auth.password_verification.unexpected_error", error=e
            )
            raise InvalidCredentialsError("invalid credentials") from e

    @staticmethod
    async def hash_password(password: str) -> str:
        """Hashes password"""

        hasher = argon2.PasswordHasher()
        return hasher.hash(password)
