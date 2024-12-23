from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base 

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    bonus_card = relationship("BonusCard", back_populates="user", cascade="all, delete")
    main_card = relationship("MainCard", back_populates="user", cascade="all, delete")



class BonusCard(Base):
    __tablename__ = "bouns_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    percent = Column(Integer)
    replenishment_time = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="bouns_cards")

class MainCard(Base):
    __tablename__ = "main_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    money = Column(Integer)
    percent = Column(Integer)
    replenishment_time = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="main_cards")

    
    