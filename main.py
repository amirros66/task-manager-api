from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from dotenv import load_dotenv
from typing import List

from app import database, schemas, users, tasks
from app.schemas import UserBase, UserCreate, UserCredentials, User
from app.users import create_user
from app.deps import get_current_user
from app.tasks import delete_task_by_user

 
load_dotenv()  # take environment variables from .env.

app = FastAPI()
#Create a FastAPI "instance"


origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
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


#TASKS

#create task
@app.post("/tasks", response_model=schemas.Task)
def create_Task(
    task: schemas.TaskCreate,
    user: UserBase = Depends(get_current_user),   
    db: Session = Depends(get_db)
):
    # create the list and pass in the user_id
    return tasks.create_task(db, user_id=user.id, task=task)


#Get logged in user's tasks
@app.get("/tasks/my-tasks", response_model=List[schemas.Task])
def read_tasks(
        user: UserBase = Depends(get_current_user), # inject the current_user means you can only access if logged in
        db: Session = Depends(get_db)):
    results = tasks.get_user_tasks(db, user_id=user.id) # pass in the user_id
    if results is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

#Delete logged in user's task by task id
@app.delete("/task/{task_id}/cancel", status_code=204)
def delete_task_endpoint(
    task_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    
    delete_task_by_user(db=db, task_id=task_id, user_id=current_user.id)
    return {"message": "Task cancelled successfully"}
    


