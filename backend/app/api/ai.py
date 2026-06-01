from fastapi import APIRouter,Depends
import httpx
from app.core.config import get_settings
from app.core.deps import get_current_user

router=APIRouter(prefix="/api/ai",tags=["AI"])
settings=get_settings()
def _ok():return settings.AI_API_KEY and settings.AI_API_KEY!="sk-your-api-key-here"

@router.post("/assign")
async def suggest_assignment(task_id:int,user=Depends(get_current_user)):
    if not _ok():return {"suggestion":"AI not configured"}
    async with httpx.AsyncClient() as c:
        r=await c.post(f"{settings.AI_BASE_URL}/chat/completions",headers={"Authorization":f"Bearer {settings.AI_API_KEY}"},json={"model":settings.AI_MODEL,"messages":[{"role":"system","content":"Project management AI"},{"role":"user","content":f"Suggest assignment for task {task_id}"}],"temperature":0.5},timeout=30)
        return {"suggestion":r.json()["choices"][0]["message"]["content"]}

@router.post("/prioritize")
async def suggest_priority(project_id:int,user=Depends(get_current_user)):
    if not _ok():return {"suggestion":"AI not configured"}
    async with httpx.AsyncClient() as c:
        r=await c.post(f"{settings.AI_BASE_URL}/chat/completions",headers={"Authorization":f"Bearer {settings.AI_API_KEY}"},json={"model":settings.AI_MODEL,"messages":[{"role":"system","content":"Priority optimization AI"},{"role":"user","content":f"Suggest priorities for project {project_id}"}],"temperature":0.5},timeout=30)
        return {"suggestion":r.json()["choices"][0]["message"]["content"]}
