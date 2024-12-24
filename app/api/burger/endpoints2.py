from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import delete, select
from database.db import get_db
from database.model import *
from app.api.schema.schema import *
from typing import List


routers = APIRouter()

@routers.get(
    "/burgers/{burger_id}",
    summary="Выводить бургер по его ID",
    response_model=BurgerResponse
)
async def get_burger_by_id(burger_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Burger)
        .filter(Burger.id == burger_id)
    )

    burger = result.unique().scalar_one_or_none()
    if not burger:
        raise HTTPException(status_code=404, detail="Burger not found")

    return BurgerResponse.from_attributes(burger)


@routers.get(
    "/users/{user_id}/bonus_cards",
    summary="Выводить бонусные карты пользователя по ID",
    response_model=List[BonusCardResponse],
)
async def get_bonus_cards_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BonusCard)
        .filter(BonusCard.user_id == user_id)
    )
    bonus_cards = result.scalars().all()

    if not bonus_cards:
        raise HTTPException(status_code=404, detail="Bonus cards not found for this user")

    return [BonusCardResponse.from_attributes(card) for card in bonus_cards]


@routers.get(
    "/users/{user_id}/main_cards",
    summary="Выводить основные карты пользователя по ID",
    response_model=List[MainCardResponse],
)
async def get_main_cards_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MainCard)
        .filter(MainCard.user_id == user_id)
    )
    main_cards = result.scalars().all()

    if not main_cards:
        raise HTTPException(status_code=404, detail="Main cards not found for this user")

    return [MainCardResponse.from_attributes(card) for card in main_cards]


@routers.post(
    "/main_cards/",
    summary="Добавить основную карту",
    response_model=MainCardResponse,  
)
async def create_main_card(
    card_request: CreateMainCardRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MainCard)
        .filter(MainCard.card_number == card_request.card_number)
    )
    existing_card = result.scalar_one_or_none()
    if existing_card:
        raise HTTPException(status_code=400, detail="Main card with this number already exists")

    new_card = MainCard(
        card_number=card_request.card_number,
        money=card_request.money,
        replenishment_time=card_request.replenishment_time,
    )

    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)  

    return new_card


@routers.post(
    "/main_cards/replenish",
    summary="Пополнить карту",
    response_model=MainCardResponse,
)
async def replenish_main_card(
    replenish_request: ReplenishCardRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MainCard)
        .filter(MainCard.card_number == replenish_request.card_number)
    )
    main_card = result.scalar_one_or_none()

    if not main_card:
        raise HTTPException(status_code=404, detail="Main card not found")
    
    main_card.money += replenish_request.replenishment_money
    main_card.replenishment_time = datetime.now().date() 
    main_card.replenishment_money = replenish_request.replenishment_money  

    db.add(main_card)
    await db.commit()

    return main_card


@routers.post(
    "/bonus_cards/",
    summary="Добавить бонусную карту",
    response_model=BonusCardResponse,  
)
async def create_bonus_card(
    card_request: CreateBonusCardRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(BonusCard)
        .filter(BonusCard.card_number == card_request.card_number)
    )
    existing_card = result.scalar_one_or_none()
    if existing_card:
        raise HTTPException(status_code=400, detail="Main card with this number already exists")

    new_card = BonusCard(
        card_number=card_request.card_number,
        money=card_request.money,
        replenishment_time=card_request.replenishment_time,
    )

    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)  

    return new_card


@routers.post(
    "/purchase_burger/",
    summary="Покупать бургер",
    response_model=PurchaseBurgerResponse
)
async def purchase_burger(
    purchase_request: PurchaseBurgerRequest,
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(select(User).filter(User.id == purchase_request.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    burger_result = await db.execute(select(Burger).filter(Burger.id == purchase_request.burger_id))
    burger = burger_result.scalar_one_or_none()
    if not burger:
        raise HTTPException(status_code=404, detail="Burger not found")

    main_card_result = await db.execute(
        select(MainCard).filter(MainCard.user_id == purchase_request.user_id)
    )
    main_card = main_card_result.scalar_one_or_none()
    if not main_card or main_card.money < burger.price * purchase_request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient funds on main card")

    bonus_percentage = burger.precent  
    total_burger_price = burger.price * purchase_request.quantity
    bonus_to_add = total_burger_price * (bonus_percentage / 100)

    bonus_card_result = await db.execute(
        select(BonusCard).filter(BonusCard.user_id == purchase_request.user_id)
    )
    bonus_card = bonus_card_result.scalar_one_or_none()
    if not bonus_card:
        raise HTTPException(status_code=404, detail="Bonus card not found")

    main_card.money -= total_burger_price
    bonus_card.money += bonus_to_add

    bonus_card.replenishment_time = datetime.now().date()

    db.add(main_card)
    db.add(bonus_card)
   
    return PurchaseBurgerResponse(
        main_card_balance=main_card.money,
        bonus_card_balance=bonus_card.money,
        discount_applied=bonus_to_add
    )


