from fastapi import APIRouter, Depends
from db.models import User
from auth.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def hello_router(current_user: User = Depends(get_current_user)):
    return {"Hello": "Router"}