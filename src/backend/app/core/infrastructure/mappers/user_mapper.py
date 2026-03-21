from ...domain.models import User
from ...domain.value_objects import UserName, UserRole
from ..db_models import DBUser
from ..dto import UserDTO


class UserMapper:
    @staticmethod
    def to_domain(db_user: DBUser) -> User:
        return User(
            user_id=db_user.user_id,
            username=UserName(db_user.username),
            hashed_password=db_user.hashed_password,
            role=UserRole(db_user.role),
            created_at=db_user.created_at,
        )

    @staticmethod
    def to_orm(user: User) -> DBUser:
        return DBUser(
            user_id=user.user_id,
            username=user.username.value,
            hashed_password=user.hashed_password,
            role=user.role.value,
            created_at=user.created_at,
        )

    @staticmethod
    def to_dto(user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id,
            username=user.username.value,
            role=user.role.value,
            created_at=user.created_at,
        )
