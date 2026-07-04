from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Dict, Any
from app.database.connection import get_db_session
from app.services.recommendation import recommendation_service

router = APIRouter()

@router.get("/{work_requirement_id}", response_model=List[Dict[str, Any]])
async def get_vendor_recommendations(work_requirement_id: UUID, db: AsyncSession = Depends(get_db_session)):
    try:
        return await recommendation_service.get_recommendations(db, work_requirement_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{work_requirement_id}/report", status_code=status.HTTP_202_ACCEPTED)
async def trigger_ai_report(work_requirement_id: UUID, request: Request):
    return await recommendation_service.trigger_report(request.app.state.redis, work_requirement_id)
