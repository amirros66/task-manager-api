from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List

from app import database, schemas, users
from app.schemas import UserBase, UserCreate, UserCredentials, User
from app.users import create_user

load_dotenv()  # take environment variables from .env.

app = FastAPI()
#Create a FastAPI "instance"


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


#USERS
# sign up users
@app.post("/users", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db, user=user)