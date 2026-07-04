from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date
from typing import Optional

from app.models.document import VendorDocument

class RepositoryDocument:
    async def create(
        self, db: AsyncSession, vendor_id: UUID, document_type: str, file_path: str, expiry_date: Optional[date] = None
    ) -> VendorDocument:
        db_obj = VendorDocument(
            vendor_id=vendor_id,
            document_type=document_type,
            file_path=file_path,
            expiry_date=expiry_date,
            created_by="system"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

document_repo = RepositoryDocument()