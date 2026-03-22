from dataclasses import dataclass

from .exceptions import InvalidLengthError, InvalidRoleError


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
