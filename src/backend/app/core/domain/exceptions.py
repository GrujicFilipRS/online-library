from dataclasses import dataclass


@dataclass
class DomainError(Exception):
    """
    Base domain error.
    All domain errors must be inherited from this class.
    """

    message: str = "DomainError"


@dataclass
class InsufficientAmountError(DomainError):
    message = "InsufficientAmountError"


@dataclass
class InvalidLengthError(DomainError):
    message = "InvalidLengthError"


@dataclass
class UserAlreadyExistsError(DomainError):
    message = "UserAlreadyExistsError"


@dataclass
class UserNotFoundError(DomainError):
    message = "UserNotFoundError"


@dataclass
class InvalidRoleError(DomainError):
    message = "InvalidRoleError"


@dataclass
class AuthError(DomainError):
    message = "AuthError"


@dataclass
class InvalidCredentialsError(DomainError):
    message = "InvalidCredentialsError"


@dataclass
class InvalidAuthProviderError(DomainError):
    message = "InvalidAuthProviderError"


@dataclass
class InvalidAuthProviderUserIdError(DomainError):
    message = "InvalidAuthProviderUserIdError"


@dataclass
class AuthProviderAccountAlreadyInUseError(DomainError):
    message = "AuthProviderAccountAlreadyInUseError"


@dataclass
class AuthProviderNotLinkedError(DomainError):
    message = "AuthProviderNotLinkedError"


@dataclass
class AuthProviderUnlinkNotSafeError(DomainError):
    message = "AuthProviderUnlinkNotSafeError"
