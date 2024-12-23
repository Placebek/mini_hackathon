from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    phone_number: str
    bonus_card: str
    main_card: str