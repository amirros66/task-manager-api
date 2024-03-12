from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user