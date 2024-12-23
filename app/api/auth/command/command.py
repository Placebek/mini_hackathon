import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.auth.schema.create.create import UserCreate

from core.conf import settings
from database.model import *

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> str:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.TOKEN_EXPIRE_SECONDS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


async def get_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    return parts[1]

async def validate_access_token(access_token: str) -> str:
    payload = jwt.decode(
            access_token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    exp = payload.get("exp")
    if exp and exp < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token has expired")
    
    return username
    