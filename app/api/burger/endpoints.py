from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import delete, select
from database.db import get_db
from database.model import *
from app.api.schema.schema import *


router = APIRouter()

# @router.get(
#     "/burger",
#     summary="Выведит все бургеры",
#     response_model=List[BurgerResponse],
# )
# async def get_all_burger(
#     db
# )