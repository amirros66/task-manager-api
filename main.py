from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from dotenv import load_dotenv
from typing import List

from app import database, schemas, users
from app.schemas import UserBase, UserCreate, UserCredentials, User
from app.users import create_user
from app.deps import get_current_user

 
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



# log in users
@app.post("/users/login", response_model=schemas.Token)
def login_user(user: schemas.UserCredentials, db: Session = Depends(get_db)):
    return users.login_user(db, user=user)



# @app.post("/docslogin", response_model=schemas.Token)
# def login_with_form_data(
#     oauth_user: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = UserCredentials(email=oauth_user.username, 
#                            password=oauth_user.password)
#     return login_user(db, user=user)

@app.post("/docslogin", response_model=schemas.Token)
def login_with_form_data(
    oauth_user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_credentials = schemas.UserCredentials(email=oauth_user.username, password=oauth_user.password)
    # Call login_user with keyword arguments to avoid confusion
    return users.login_user(db=db, user=user_credentials)



@app.get("/users/profile", response_model=UserBase)
def get_user_profile(user: UserBase = Depends(get_current_user)):
    return user