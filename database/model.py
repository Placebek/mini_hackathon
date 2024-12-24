from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    bonus_cards = relationship("BonusCard", back_populates="user", cascade="all, delete")
    main_cards = relationship("MainCard", back_populates="user", cascade="all, delete")
    baskets = relationship("Basket", back_populates="user", cascade="all, delete")


class BonusCard(Base):
    __tablename__ = "bonus_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    replenishment_time = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="bonus_cards")


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

    baskets = relationship("Basket", back_populates="burger", cascade="all, delete")


class Basket(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="baskets")

    burger_id = Column(Integer, ForeignKey("burgers.id", ondelete="CASCADE"))
    burger = relationship("Burger", back_populates="baskets")

