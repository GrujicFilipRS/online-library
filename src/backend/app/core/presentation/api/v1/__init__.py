from fastapi import APIRouter

from .routers import routers

api_v1_router = APIRouter(prefix="/api/v1")

for router in routers:
    api_v1_router.include_router(router)
