from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from .....application.use_cases.user.register_via_password import (
    RegisterViaPasswordUseCase,
)
from .....infrastructure.mappers import UserMapper
from ..schemas.users_schemas import (
    RegisterViaPasswordRequestSchema,
    RegisterViaPasswordResponseSchema,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@auth_router.post(
    "/register_via_password", response_model=RegisterViaPasswordResponseSchema
)
@inject
async def register_via_password(
    user_data: RegisterViaPasswordRequestSchema,
    user_register: FromDishka[RegisterViaPasswordUseCase],
):
    username, password = user_data.username, user_data.password
    user = await user_register.execute(username, password)
    user_dto = UserMapper.to_dto(user)
    return {
        "success": True,
        "message": "successfully registered new user",
        "user": user_dto,
    }
