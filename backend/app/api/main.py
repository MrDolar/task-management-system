"""API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, get_admin_user
from app.models.main_models import *

router = APIRouter(prefix="/api", tags=["Main"])

@router.get("/projects")
async def list_projects(user = Depends(get_current_user), db = Depends(get_db)):
    return db.query(Project).filter(Project.owner_id == user.id).all()

@router.post("/projects", status_code=201)
async def create_project(name: str, description: str = "", user = Depends(get_current_user), db = Depends(get_db)):
    p = Project(name=name, description=description, owner_id=user.id)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/tasks")
async def list_tasks(project_id: int = None, status: str = None, db = Depends(get_db)):
    query = db.query(Task)
    if project_id: query = query.filter(Task.project_id == project_id)
    if status: query = query.filter(Task.status == status)
    return query.all()

@router.post("/tasks", status_code=201)
async def create_task(title: str, project_id: int, priority: str = "medium", db = Depends(get_db)):
    t = Task(title=title, project_id=project_id, priority=priority)
    db.add(t); db.commit(); db.refresh(t)
    return t

@router.put("/tasks/{id}/status")
async def update_status(id: int, status: str, db = Depends(get_db)):
    t = db.query(Task).filter(Task.id == id).first()
    if not t: raise HTTPException(404)
    t.status = status; db.commit()
    return {"message": "updated"}
