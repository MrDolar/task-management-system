"""Task Management System"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api import auth, main as main_api

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(title="Task Management System", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(main_api.router)

@app.get("/")
async def root():
    return {"name": "Task Management System", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok"}
