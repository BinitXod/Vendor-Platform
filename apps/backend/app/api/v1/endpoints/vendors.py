from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db_session
from app.schemas.common import Page
from app.schemas.document import DocumentResponse
from app.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate
from app.services.vendor import vendor_service

router = APIRouter()


@router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(vendor_in: VendorCreate, db: AsyncSession = Depends(get_db_session)):
    return await vendor_service.create_vendor(db, vendor_in=vendor_in)


@router.get("", response_model=Page[VendorResponse])
async def list_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
):
    items, total = await vendor_service.list_vendors(db, skip=skip, limit=limit)
    return Page[VendorResponse](items=items, total=total, skip=skip, limit=limit)


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await vendor_service.get_vendor(db, vendor_id)


@router.patch("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    vendor_id: UUID,
    vendor_in: VendorUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    return await vendor_service.update_vendor(db, vendor_id, vendor_in)


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(vendor_id: UUID, db: AsyncSession = Depends(get_db_session)):
    await vendor_service.delete_vendor(db, vendor_id)


@router.post("/{vendor_id}/documents", response_model=DocumentResponse)
async def upload_document(
    vendor_id: UUID,
    document_type: str = Form(...),
    expiry_date: Optional[date] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
):
    return await vendor_service.upload_document(
        db,
        vendor_id=vendor_id,
        document_type=document_type,
        expiry_date=expiry_date,
        file=file,
    )
