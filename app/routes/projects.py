from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/", response_model=list[schemas.Project])
def get_projects(user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    return db.query(models.Project).filter(models.Project.owner_id == user.id).all()


@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    db_project = models.Project(**project.dict(), owner_id=user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, updated: schemas.ProjectCreate, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = updated.name
    project.description = updated.description
    db.commit()
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, user=Depends(get_current_user), db: Session = Depends(database.SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted"}
