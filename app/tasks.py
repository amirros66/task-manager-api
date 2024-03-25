from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime





def create_task(db: Session, user_id: int, task: schemas.TaskCreate):
    # Assuming task is an instance of schemas.TaskCreate and has the necessary task details.
    db_task = models.Task(**task.dict(), owner_id=user_id)
    
    db.add(db_task)
    db.commit()  # This commits the transaction, making the object persistent.
    db.refresh(db_task)  # This refreshes the instance from the database.
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


