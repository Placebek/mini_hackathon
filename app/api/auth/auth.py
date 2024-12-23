from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.command.command import get_user, hash_password, verify_password, create_access_token
from app.api.auth.schema.create.create import UserCreate

from model.model import *
from database.db import get_db


router = APIRouter()


@router.post(
    "/login", 
    response_model=Token
)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user.username)

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
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User registered successfully"}



# @router.get("/examination")
# async def protected_route(current_user: UserData = Depends(get_current_user)):
#     return {"message": f"Привет, {current_user.username}! Это защищённый маршрут."}


# @router.get("/examination")
# async def protected_route(token: str, db: AsyncSession = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         user = await get_user(db, username)
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")
#         return {"message": f"Hello, {username}!"}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")