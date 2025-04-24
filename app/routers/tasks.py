from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.models import User, Task
from db import models
from db.database import SessionLocal
from auth.deps import get_current_user
from db.schemas import TaskResponse, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

#Maneja la creacion de la sesion de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TaskResponse])
async def all_tasks(current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@router.post("/create_task")
async def create_task(task_data: TaskCreate,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    
    task = models.Task(
        title = task_data.title,
        description = task_data.description,
        user_id = current_user.id
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {"message": "Tarea creada con exito!", "title": task.title, "description": task.description}

@router.put("/update_task/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int,
                      task_update: TaskCreate,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta tarea")

    task.title = task_update.title
    task.description = task_update.description
    
    db.commit()
    db.refresh(task)
    
    return task

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id: int,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta tarea")
    
    db.delete(task)
    db.commit()
    
    return {"Message": "Tarea eliminada con exito"}