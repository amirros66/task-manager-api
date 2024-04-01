from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime





def create_task(db: Session, user_id: int, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    
    db.add(db_task)
    db.commit()  
    db.refresh(db_task)  
    return db_task


#get logged in user's tasks
def get_user_tasks(db: Session, user_id: int):
    tasks = db.query(models.Task).filter(
        models.Task.owner_id == user_id).all()
    return tasks

#Delete task
def delete_task_by_user(db: Session, user_id: int, task_id: int):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id,
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()


#Update task status

    
def update_task_status(db: Session, user_id: int, task_id: int, new_status: str):
    if new_status.lower() not in [status.value for status in models.TaskStatus]:
        raise HTTPException(status_code=400, detail="Invalid status provided")

    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = models.TaskStatus(new_status.lower())
    db.commit()
    return task
