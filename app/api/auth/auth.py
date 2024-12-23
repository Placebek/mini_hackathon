from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.command.command import get_access_token, get_user, hash_password, validate_access_token, verify_password, create_access_token
from app.api.auth.schema.create.create import UserCreate

from app.api.auth.schema.response.response import TokenResponse, UserResponse
from model.model import *
from database.db import get_db


router = APIRouter()


@router.post(
    "/login", 
    response_model=TokenResponse
)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(username=user.username, db=db)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    existing_user = await get_user(db, user.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, phone_number=user.phone_number)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.get(
    '/profile',
    summary="get user profile data",
    response_model=UserResponse
)
async def user_profile(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        username = await validate_access_token(access_token=access_token)

        user = await get_user(username=username, db=db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
