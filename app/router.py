from fastapi import APIRouter

from mini_hackathon.app.api.burger.endpoints import router as burger_router

route = APIRouter()


route.include_router(burger_router, prefix="/burger", tags=["burger"])