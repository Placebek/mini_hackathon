from datetime import datetime

from sqlalchemy import Column, Date, Integer, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.db import Base 

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    bonus_card = relationship("BonusCard", back_populates="user", cascade="all, delete")
    main_card = relationship("MainCard", back_populates="user", cascade="all, delete")


class BonusCard(Base):
    __tablename__ = "bonus_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    replenishment_time = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.now)


    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="bonus_cards")
    
    burger_id = Column(Integer, ForeignKey("burger.id", ondelete="CASCADE"))
    burger = relationship("Burger", back_populates="burgers")


class MainCard(Base):
    __tablename__ = "main_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    replenishment_time = Column(Date)
    replenishment_money = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="main_cards")

    
class Burger(Base):
    __tablename__ = "burgers"

    id = Column(Integer, primary_key=True, index=True)
    name_burger = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    precent = Column(Float, nullable=False)

    bonus_id = Column(Integer, ForeignKey("bonus.id", ondelete="CASCADE"))
    bonus = relationship("BonusCard", back_populates="bonus_cards")