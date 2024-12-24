from pydantic import BaseModel, HttpUrl
from datetime import datetime, date
from typing import List, Optional


class BurgerBase(BaseModel):
    burger_name: str

    class Config:
        orm_mode = True


class BurgerCreate(BurgerBase):
    pass


class BurgerResponse(BaseModel):
    id: int
    name_burger: str
    price: float
    created_at: datetime
    precent: float

    class Config:
        orm_mode = True


class BurgerUpdate(BaseModel):
    burger_name: str


class PurchaseBurgerRequest(BaseModel):
    burger_id: int
    user_id: int
    quantity: int

    class Config:
        orm_mode = True


class PurchaseBurgerResponse(BaseModel):
    main_card_balance: int
    bonus_card_balance: int
    discount_applied: float

    class Config:
        orm_mode = True


class BonusCardResponse(BaseModel):
    id: int
    card_number: str
    money: Optional[int] = None
    replenishment_time: Optional[date] = None
    created_at: datetime

    class Config:
        orm_mode = True


class CreateBonusCardRequest(BaseModel):
    card_number: str  
    money: Optional[int] = 0  
    replenishment_time: Optional[date] = None  
    replenishment_money: Optional[int] = None  

    class Config:
        orm_mode = True


class MainCardResponse(BaseModel):
    id: int
    card_number: str
    money: Optional[int] = None
    replenishment_time: Optional[date] = None
    replenishment_money: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ReplenishCardRequest(BaseModel):
    card_number: str  
    replenishment_money: int 

    class Config:
        orm_mode = True


class CreateMainCardRequest(BaseModel):
    card_number: str  
    money: Optional[int] = 0  
    replenishment_time: Optional[date] = None    

    class Config:
        orm_mode = True


class BasketResponse(BaseModel):
    id: int
    created_at: datetime

    burger: List[BurgerResponse] 

    class Config:
        orm_mode = True


class BasketRequest(BaseModel):
    user_id: int
    burger_id: int
    
    class Config:
        prm_mode = True