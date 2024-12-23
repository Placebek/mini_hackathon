from datetime import datetime

from sqlalchemy import Column, Date, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from database.db import Base 

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    bonus_card = relationship("BonusCard", back_populates="user", cascade="all, delete")
    main_card = relationship("MainCard", back_populates="user", cascade="all, delete")



class BonusCard(Base):
    __tablename__ = "bouns_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    percent = Column(Integer)
    replenishment_time = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.now)


    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="bouns_cards")

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

    
    