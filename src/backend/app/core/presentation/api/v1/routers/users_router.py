from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordBearer

from ......shared.infra.dto import BaseResponseDTO
from ......shared.utils.auth import CookiesUtils
from .....application.use_cases.user import (
    LoginViaPasswordUseCase,
    RegisterViaPasswordUseCase,
)
from .....infrastructure.mappers import UserMapper
from ..schemas import (
    LoginViaPasswordRequestSchema,
    RegisterViaPasswordRequestSchema,
    RegisterViaPasswordResponseSchema,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login_via_password")

auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@auth_router.post(
    "/register_via_password", response_model=RegisterViaPasswordResponseSchema
)
@inject
async def register_via_password(
    user_data: RegisterViaPasswordRequestSchema,
    register_via_password: FromDishka[RegisterViaPasswordUseCase],
):
    username, password = user_data.username, user_data.password
    user = await register_via_password.execute(username, password)
    user_dto = UserMapper.to_dto(user)
    return {
        "success": True,
        "message": "successfully registered new user",
        "user": user_dto,
    }


@auth_router.post("/login_via_password", response_model=BaseResponseDTO)
@inject
async def login_via_password(
    user_data: LoginViaPasswordRequestSchema,
    login_via_password: FromDishka[LoginViaPasswordUseCase],
    response: Response,
):
    username, password = user_data.username, user_data.password
    access_token, refresh_token, csrf_token = await login_via_password.execute(
        username, password
    )
    CookiesUtils.set_auth_cookies(response, access_token, refresh_token, csrf_token)
    return {
        "success": True,
        "message": "successfully logged in",
    }
