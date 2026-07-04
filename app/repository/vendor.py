from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from uuid import UUID
from typing import Optional

from app.repository.base import BaseRepository
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate

class RepositoryVendor(BaseRepository[Vendor, VendorCreate, VendorUpdate]):
    async def get_with_documents(self, db: AsyncSession, vendor_id: UUID) -> Optional[Vendor]:
        # selectinload eagerly fetches the related documents to avoid N+1 query problems
        query = (
            self._active()
            .options(selectinload(Vendor.documents))
            .filter(Vendor.id == vendor_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Vendor]:
        """Fetch a vendor by their unique email address (active rows only)."""
        query = self._active().filter(Vendor.contact_email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def list_with_documents(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[Vendor]:
        query = (
            self._active()
            .options(selectinload(Vendor.documents))
            .order_by(Vendor.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create_with_embedding(
        self,
        db: AsyncSession,
        *,
        obj_in: VendorCreate,
        embedding: Sequence[float],
        created_by: str = "system"
    ) -> Vendor:
        vendor_data = obj_in.model_dump()
        db_obj = Vendor(**vendor_data, semantic_profile=list(embedding), created_by=created_by)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj, ["documents"])
        return db_obj

    async def get_recommendation_candidates(
        self,
        db: AsyncSession,
        *,
        location: str,
        query_vector: Sequence[float]
    ) -> list[tuple[Vendor, float]]:
        distance_col = Vendor.semantic_profile.cosine_distance(list(query_vector)).label("distance")
        query = (
            select(Vendor, distance_col)
            .options(selectinload(Vendor.documents))
            .filter(
                Vendor.deleted_at.is_(None),
                Vendor.current_status == "Active",
                Vendor.operating_location == location
            )
        )
        result = await db.execute(query)
        return list(result.all())

vendor_repo = RepositoryVendor(Vendor)
