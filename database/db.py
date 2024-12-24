from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from core.conf import settings


DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async_engine = create_async_engine(
    settings.DATABASE_URL_asyncpg, 
    echo=False
)

SessionLocal = async_sessionmaker(
    bind=async_engine, 
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session