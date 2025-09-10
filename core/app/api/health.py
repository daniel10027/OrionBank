from fastapi import APIRouter
from core.app.schemas.common import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")