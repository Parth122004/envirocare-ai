from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    created_at: datetime = datetime.utcnow()

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
