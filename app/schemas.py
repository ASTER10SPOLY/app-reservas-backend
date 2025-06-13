# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Auth ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

# --- Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# --- Profile ---
class ProfileBase(BaseModel):
    username: Optional[str]
    description: Optional[str]
    position: Optional[str]
    avatar_url: Optional[str]

class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    user_id: int
    class Config:
        orm_mode = True
