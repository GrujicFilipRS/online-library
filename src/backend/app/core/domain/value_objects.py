from dataclasses import dataclass

from .exceptions import (
    InvalidAuthProviderError,
    InvalidAuthProviderUserIdError,
    InvalidLengthError,
    InvalidRoleError,
)


@dataclass
class UserName:
    value: str

    def __post_init__(self):
        minimum_username_length, maximum_username_length = 6, 25
        if (
            len(self.value) < minimum_username_length
            or len(self.value) > maximum_username_length
        ):
            raise InvalidLengthError(
                f"username must be from {minimum_username_length} to {maximum_username_length} characters long"
            )


@dataclass
class UserRole:
    value: str

    def __post_init__(self):
        possible_roles = ("User", "Admin")

        if self.value not in possible_roles:
            raise InvalidRoleError(
                f"user role must be one of the following: {', '.join(possible_roles)}"
            )


@dataclass(frozen=True)
class AuthProvider:
    value: str

    def __post_init__(self):
        possible_providers = ("google", "github", "apple")
        if self.value not in possible_providers:
            raise InvalidAuthProviderError(
                f"Auth provider must be on of the following: {', '.join(possible_providers)}"
            )


@dataclass(frozen=True)
class AuthProviderUserId:
    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise InvalidAuthProviderUserIdError(
                "Auth provider user id must not be empty"
            )
