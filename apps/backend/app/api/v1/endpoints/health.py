from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": "v1"
    }