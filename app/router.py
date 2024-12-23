from fastapi import APIRouter

from app.api.burger.endpoints import router as burger_router
from app.api.auth.auth import router as auth_router

route = APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(burger_router, prefix="/burger", tags=["burger"])