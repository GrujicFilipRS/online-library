from fastapi import APIRouter

from .routers import *

api_v1_router = APIRouter(prefix="/api/v1")
