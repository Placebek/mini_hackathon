from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import delete, select
from database.db import get_db
from database.model import *
from app.api.schema.schema import *
from typing import List


router = APIRouter()


@router.get(
    "/bonus_cards",
    summary="Выводить все бонусные карты",
    response_model=List[BonusCardResponse],
)
async def get_all_bonus_cards(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(BonusCard).offset(skip).limit(limit)
    )
    bonus_cards = result.scalars().all()
    return [BonusCardResponse.from_attributes(card) for card in bonus_cards]


@router.get(
    "/main_cards",
    summary="Выводить все основные карты",
    response_model=List[MainCardResponse],
)
async def get_all_main_cards(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(MainCard).offset(skip).limit(limit)
    )
    main_cards = result.scalars().all()
    return [MainCardResponse.from_attributes(card) for card in main_cards]


@router.get(
    "/burgers",
    summary="Выводить все бургеры",
    response_model=List[BurgerResponse],
)
async def get_all_burgers(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Burger).offset(skip).limit(limit)
    )
    burgers = result.scalars().all()
    return [BurgerResponse.from_attributes(burger) for burger in burgers]