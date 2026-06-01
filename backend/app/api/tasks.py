from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.task import Task

router=APIRouter(prefix="/api/tasks",tags=["Tasks"])

class TaskCreate(BaseModel):
    title:str;description:str="";project_id:int;assignee_id:Optional[int]=None;status:str="todo";priority:str="medium";due_date:Optional[datetime]=None;tags:str=""

@router.get("")
async def list_tasks(project_id:Optional[int]=None,status:Optional[str]=None,db:Session=Depends(get_db)):
    q=db.query(Task)
    if project_id:q=q.filter(Task.project_id==project_id)
    if status:q=q.filter(Task.status==status)
    return {"items":[{"id":t.id,"title":t.title,"status":t.status,"priority":t.priority,"project_id":t.project_id} for t in q.order_by(Task.created_at.desc()).all()]}

@router.post("")
async def create_task(req:TaskCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    t=Task(**req.dict());db.add(t);db.commit();db.refresh(t);return {"id":t.id,"title":t.title}

@router.put("/{tid}/status")
async def update_status(tid:int,status:str,db:Session=Depends(get_db)):
    t=db.query(Task).filter(Task.id==tid).first()
    if not t:raise HTTPException(404,"Not found")
    t.status=status;db.commit();return {"id":t.id,"status":t.status}

@router.delete("/{tid}")
async def delete_task(tid:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    t=db.query(Task).filter(Task.id==tid).first()
    if not t:raise HTTPException(404,"Not found")
    db.delete(t);db.commit();return {"message":"Deleted"}
