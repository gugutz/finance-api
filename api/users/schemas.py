
from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Token Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---

# Base properties for a user
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties stored in DB
class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True # Formerly orm_mode

# Properties to return to client
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # Formerly orm_mode
