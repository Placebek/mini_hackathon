from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from jose import jwt, JOSEError
from typing import Dict
import os
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
app = FastAPI()


@app.middleware('http')
async def middleware(request: Request, call_next):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = token.replace("Bearer ", "")

    try:
        token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except JOSEError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = token_parts.get('k')  
    if not user_id:
        raise HTTPException(status_code=403, detail="User not found")
    
    response = await call_next(request)
    return response
