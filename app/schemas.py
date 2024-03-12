from pydantic import BaseModel, model_validator
from datetime import datetime, time
from typing import Optional


#USERS
class UserBase(BaseModel):
    id: int
    email: str

class UserCreate(BaseModel):
    email: str
    password: str


class UserCredentials(BaseModel):
    email: str
    password: str


class User(UserBase):
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: int
    sub: str
