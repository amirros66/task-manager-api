from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum  

from datetime import datetime, time


from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    disabled = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=True)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.TODO)  

    # Foreign key, task is associated with user.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship, task belongs to a user
    owner = relationship("User", back_populates="tasks")

 #pipenv run alembic revision --autogenerate -m "First revision"
#pipenv run alembic upgrade head
