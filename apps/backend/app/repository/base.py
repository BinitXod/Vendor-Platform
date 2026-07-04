from datetime import datetime, timezone
from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _active(self):
        """Base query that excludes soft-deleted rows."""
        return select(self.model).filter(self.model.deleted_at.is_(None))

    async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
        result = await db.execute(self._active().filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        query = (
            self._active()
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count(self, db: AsyncSession) -> int:
        query = select(func.count()).select_from(self.model).filter(
            self.model.deleted_at.is_(None)
        )
        result = await db.execute(query)
        return int(result.scalar_one())

    async def create(
        self, db: AsyncSession, *, obj_in: CreateSchemaType, created_by: str = "system"
    ) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(), created_by=created_by)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        updated_by: str = "system",
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db_obj.updated_by = updated_by
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(
        self, db: AsyncSession, *, db_obj: ModelType, deleted_by: str = "system"
    ) -> ModelType:
        db_obj.deleted_at = datetime.now(timezone.utc)
        db_obj.updated_by = deleted_by
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
