from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.task import Project

router=APIRouter(prefix="/api/projects",tags=["Projects"])

class ProjectCreate(BaseModel):
    name:str;description:str=""

@router.get("")
async def list_projects(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return {"items":[{"id":p.id,"name":p.name,"status":p.status} for p in db.query(Project).filter(Project.owner_id==user.id).all()]}

@router.post("")
async def create_project(req:ProjectCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=Project(**req.dict(),owner_id=user.id);db.add(p);db.commit();db.refresh(p);return {"id":p.id,"name":p.name}

@router.delete("/{pid}")
async def delete_project(pid:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=db.query(Project).filter(Project.id==pid,Project.owner_id==user.id).first()
    if not p:raise HTTPException(404,"Not found")
    db.delete(p);db.commit();return {"message":"Deleted"}
