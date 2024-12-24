import hmac 
import hashlib
from typing import Annotated
from fastapi import APIRouter, Query, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from jose import jwt
import os
from dotenv import load_dotenv


load_dotenv()

auth_router = APIRouter()
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
BOT_TOKEN_HASH = hashlib.sha256(os.environ['BOT_TOKEN'].encode())
COOKIE_NAME = 'auth-token'
USER_DATABASE = {}


@auth_router.get('/telegram-callback')
async def telegram_callback(
    request: Request,
    user_id: Annotated[int, Query(alias='id')],
    username: Annotated[str, Query(alias='username')],
    query_hash: Annotated[str, Query(alias='hash')],
):
    params = request.query_params.items()
    data_check_string = '\n'.join(sorted(f'{x}={y}' for x,y in params if x not in ('hash')))
    computed_hash = hmac.new(BOT_TOKEN_HASH.encode(), data_check_string.encode(), 'sha256').hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)
    if not is_correct:
        raise HTTPException(status_code=401, detail="Authorization failed. Please try again")
    
    if user_id in USER_DATABASE:
        raise HTTPException(status_code=400, detail="User already registered.")
    
    USER_DATABASE[user_id] = {'username': username}

    token = jwt.encode(
        {'alg': 'HS256'},
        {'k': user_id},
        JWT_SECRET_KEY
    )

    return JSONResponse(content={'token': token, 'username': username})


@auth_router.get('/login')
async def login(
    username: Annotated[str, Query()],
):
    user = next((user for user_id, user in USER_DATABASE.items() if user['username'] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = jwt.encode(
        {'alg': 'HS256'},
        {'k': user_id},  
        JWT_SECRET_KEY
    )

    return JSONResponse(content={"token": token, "username": username})


@auth_router.get('/logout')
async def logout():
    return JSONResponse(content={'message': "Logged out successfully."}, status_code=200)
