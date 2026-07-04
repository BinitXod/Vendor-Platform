from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db_session
from app.schemas.common import Page
from app.schemas.work_requirement import (
    WorkRequirementCreate,
    WorkRequirementResponse,
    WorkRequirementUpdate,
)
from app.services.work_requirement import work_requirement_service

router = APIRouter()


@router.post("", response_model=WorkRequirementResponse, status_code=status.HTTP_201_CREATED)
async def create_work_requirement(
    work_in: WorkRequirementCreate, db: AsyncSession = Depends(get_db_session)
):
    return await work_requirement_service.create_work_requirement(db, work_in)


@router.get("", response_model=Page[WorkRequirementResponse])
async def list_work_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
):
    items, total = await work_requirement_service.list_work_requirements(
        db, skip=skip, limit=limit
    )
    return Page[WorkRequirementResponse](items=items, total=total, skip=skip, limit=limit)


@router.get("/{work_req_id}", response_model=WorkRequirementResponse)
async def get_work_requirement(
    work_req_id: UUID, db: AsyncSession = Depends(get_db_session)
):
    work = await work_requirement_service.get_work_requirement(db, work_req_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Work requirement not found"
        )
    return work


@router.patch("/{work_req_id}", response_model=WorkRequirementResponse)
async def update_work_requirement(
    work_req_id: UUID,
    work_in: WorkRequirementUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    return await work_requirement_service.update_work_requirement(db, work_req_id, work_in)


@router.delete("/{work_req_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_requirement(
    work_req_id: UUID, db: AsyncSession = Depends(get_db_session)
):
    await work_requirement_service.delete_work_requirement(db, work_req_id)
