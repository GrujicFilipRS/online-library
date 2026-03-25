from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter, Response

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

auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@auth_router.post(
    "/register_via_password", response_model=RegisterViaPasswordResponseSchema
)
@inject
async def register_via_password(
    user_data: RegisterViaPasswordRequestSchema,
    register_usecase: FromDishka[RegisterViaPasswordUseCase],
    response: Response,
):
    username, password = user_data.username, user_data.password
    user, access_token, refresh_token, csrf_token = await register_usecase.execute(
        username, password
    )
    user_dto = UserMapper.to_dto(user)

    CookiesUtils.set_auth_cookies(response, access_token, refresh_token, csrf_token)

    return {
        "success": True,
        "message": "successfully registered new user",
        "code": "Success",
        "user": user_dto,
    }


@auth_router.post("/login_via_password", response_model=BaseResponseDTO)
@inject
async def login_via_password(
    user_data: LoginViaPasswordRequestSchema,
    login_usecase: FromDishka[LoginViaPasswordUseCase],
    response: Response,
):
    username, password = user_data.username, user_data.password
    access_token, refresh_token, csrf_token = await login_usecase.execute(
        username, password
    )
    CookiesUtils.set_auth_cookies(response, access_token, refresh_token, csrf_token)
    return {
        "success": True,
        "message": "successfully logged in",
        "code": "Success",
    }
