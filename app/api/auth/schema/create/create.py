from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    phone_number: str
    # bonus_card: str
    # main_card: str