from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    disabled = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="tasks")