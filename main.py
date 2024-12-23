from fastapi import FastAPI
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.middleware.cors import CORSMiddleware

from app.router import route

app = FastAPI()

app.include_router(route)
