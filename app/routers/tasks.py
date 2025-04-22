from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def hello_router():
    return {"Hello": "Router"}