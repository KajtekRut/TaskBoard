from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.routes.projects import get_current_user
from app.websocket import notify_all

router = APIRouter()


@router.get("/", response_model=list[schemas.Task])
def get_tasks(user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    return db.query(models.Task).join(models.Project).filter(models.Project.owner_id == user.id).all()


@router.post("/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == task.project_id, models.Project.owner_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    await notify_all(f"New task added: {db_task.name} in project '{project.name}'")

    return db_task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, updated: schemas.TaskCreate, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id, models.Project.owner_id == user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.name = updated.name
    task.status = updated.status
    task.deadline = updated.deadline
    task.project_id = updated.project_id
    db.commit()
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id, models.Project.owner_id == user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
