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


#Tasks

class TaskBase(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class TaskCreate(BaseModel):
    title: str



class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  # Allow None as a valid value
    created_at: datetime
    due_date: Optional[datetime] = None  # Allow None as a valid value
    completed: bool
    owner: User

    class Config:
        orm_mode = True