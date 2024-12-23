from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.conf import settings

class Base(DeclarativeBase):
    pass


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