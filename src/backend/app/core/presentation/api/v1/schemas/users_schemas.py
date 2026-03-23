from pydantic import BaseModel

from .....infrastructure.dto.users_dto import UserDTO


class RegisterViaPasswordRequestSchema(BaseModel):
    username: str
    password: str


class RegisterViaPasswordResponseSchema(BaseModel):
    success: bool
    message: str
    user: UserDTO