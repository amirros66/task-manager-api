from pydantic import BaseModel, model_validator
from datetime import datetime, time
from typing import Optional
from app.models import TaskStatus


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
    title: str
    # description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    # description: Optional[str] = None
    status: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    due_date: Optional[datetime] = None
    status: str  
    owner_id: int

    class Config:
        orm_mode = True



class TaskUpdateStatus(BaseModel):
    status: Optional[TaskStatus]