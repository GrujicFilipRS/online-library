from pydantic import BaseModel

from ......shared.infra.dto import BaseResponseDTO
from .....infrastructure.dto.users_dto import UserDTO


class RegisterViaPasswordRequestSchema(BaseModel):
    username: str
    password: str


class RegisterViaPasswordResponseSchema(BaseResponseDTO):
    user: UserDTO


class LoginViaPasswordRequestSchema(BaseModel):
    username: str
    password: str
