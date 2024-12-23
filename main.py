from fastapi import FastAPI

from app.router import route as burger_route

from database.db import Base, async_engine

app = FastAPI()

app.include_router(burger_route)
