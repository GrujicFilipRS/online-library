from fastapi import APIRouter

from .routers import *

api_v1_router = APIRouter(prefix="/api/v1")

from .routers.users_router import auth_router as users_auth_router
api_v1_router.include_router(users_auth_router)