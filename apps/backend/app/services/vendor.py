import os
import shutil
from datetime import date
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import VendorDocument
from app.schemas.vendor import VendorCreate, VendorUpdate
from app.models.vendor import Vendor
from app.repository.document import document_repo
from app.repository.vendor import vendor_repo
from app.config.settings import settings
from app.services.ai import generate_vendor_embedding
from app.utils.logger import logger

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


class VendorService:
    @staticmethod
    async def create_vendor(db: AsyncSession, vendor_in: VendorCreate) -> Vendor:
        # 0. Check if email already exists in the database
        existing_vendor = await vendor_repo.get_by_email(db, vendor_in.contact_email)
        if existing_vendor:
            logger.warning(f"Attempted to register duplicate vendor email: {vendor_in.contact_email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A vendor with email '{vendor_in.contact_email}' already exists."
            )

        # 1. Prepare the text payload for the AI
        # We combine Category and Capabilities for a richer semantic profile
        ai_text_payload = f"Category: {vendor_in.category}. Capabilities: {vendor_in.capabilities_description or 'Standard services.'}"

        # 2. Call the AI Service to get the embedding
        logger.info(f"Generating semantic embedding for vendor: {vendor_in.name}")
        embedding = await generate_vendor_embedding(ai_text_payload)

        # 3. Persist the vendor with the generated embedding
        return await vendor_repo.create_with_embedding(db, obj_in=vendor_in, embedding=embedding)

    @staticmethod
    async def get_vendor(db: AsyncSession, vendor_id: UUID) -> Vendor:
        vendor = await vendor_repo.get_with_documents(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        return vendor

    @staticmethod
    async def list_vendors(
        db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> tuple[list[Vendor], int]:
        items = await vendor_repo.list_with_documents(db, skip=skip, limit=limit)
        total = await vendor_repo.count(db)
        return items, total

    @staticmethod
    async def update_vendor(
        db: AsyncSession, vendor_id: UUID, vendor_in: VendorUpdate
    ) -> Vendor:
        vendor = await vendor_repo.get_with_documents(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

        updated = await vendor_repo.update(db, db_obj=vendor, obj_in=vendor_in)

        # If capabilities text changed, refresh the semantic embedding.
        if vendor_in.model_dump(exclude_unset=True).get("capabilities_description") is not None:
            ai_text_payload = (
                f"Category: {updated.category}. "
                f"Capabilities: {updated.capabilities_description or 'Standard services.'}"
            )
            embedding = await generate_vendor_embedding(ai_text_payload)
            if embedding is not None:
                updated.semantic_profile = list(embedding)
                db.add(updated)
                await db.commit()
                await db.refresh(updated, ["documents"])
        return updated

    @staticmethod
    async def delete_vendor(db: AsyncSession, vendor_id: UUID) -> None:
        vendor = await vendor_repo.get(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        await vendor_repo.soft_delete(db, db_obj=vendor)

    @staticmethod
    async def upload_document(
        db: AsyncSession,
        *,
        vendor_id: UUID,
        document_type: str,
        file: UploadFile,
        expiry_date: Optional[date] = None
    ) -> VendorDocument:
        vendor = await vendor_repo.get(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

        original_filename = Path(file.filename or "document").name
        safe_filename = f"{vendor_id}_{original_filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return await document_repo.create(
            db=db,
            vendor_id=vendor_id,
            document_type=document_type,
            file_path=file_path,
            expiry_date=expiry_date
        )


vendor_service = VendorService()
