from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import init_db
@asynccontextmanager
async def lifespan(a:FastAPI):init_db();yield
app=FastAPI(title="Task Management",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
from app.api import auth,tasks,projects,ai
app.include_router(auth.router);app.include_router(tasks.router);app.include_router(projects.router);app.include_router(ai.router)
@app.get("/")
async def root():return {"name":"Task Management","docs":"/docs"}
