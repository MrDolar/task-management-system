from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from app.core.database import Base

class Project(Base):
    __tablename__="projects"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    description=Column(Text,default="")
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    status=Column(String(20),default="active")
    created_at=Column(DateTime,default=datetime.utcnow)

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(200),nullable=False)
    description=Column(Text,default="")
    project_id=Column(Integer,ForeignKey("projects.id"),nullable=False)
    assignee_id=Column(Integer,ForeignKey("users.id"),nullable=True)
    status=Column(String(20),default="todo")
    priority=Column(String(10),default="medium")
    due_date=Column(DateTime,nullable=True)
    tags=Column(String(200),default="")
    created_at=Column(DateTime,default=datetime.utcnow)
