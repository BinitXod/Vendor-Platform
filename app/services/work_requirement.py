from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.work_requirement import WorkRequirement
from app.repository.work_requirement import work_req_repo
from app.schemas.work_requirement import WorkRequirementCreate, WorkRequirementUpdate


class WorkRequirementService:
    @staticmethod
    async def create_work_requirement(
        db: AsyncSession, work_in: WorkRequirementCreate
    ) -> WorkRequirement:
        return await work_req_repo.create(db, obj_in=work_in)

    @staticmethod
    async def get_work_requirement(
        db: AsyncSession, work_req_id: UUID
    ) -> WorkRequirement | None:
        return await work_req_repo.get(db, work_req_id)

    @staticmethod
    async def list_work_requirements(
        db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkRequirement], int]:
        items = await work_req_repo.get_multi(db, skip=skip, limit=limit)
        total = await work_req_repo.count(db)
        return items, total

    @staticmethod
    async def update_work_requirement(
        db: AsyncSession, work_req_id: UUID, work_in: WorkRequirementUpdate
    ) -> WorkRequirement:
        work = await work_req_repo.get(db, work_req_id)
        if not work:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Work requirement not found",
            )
        return await work_req_repo.update(db, db_obj=work, obj_in=work_in)

    @staticmethod
    async def delete_work_requirement(db: AsyncSession, work_req_id: UUID) -> None:
        work = await work_req_repo.get(db, work_req_id)
        if not work:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Work requirement not found",
            )
        await work_req_repo.soft_delete(db, db_obj=work)


work_requirement_service = WorkRequirementService()
