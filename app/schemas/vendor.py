from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.document import DocumentResponse

class VendorBase(BaseModel):
    name: str
    vendor_type: str
    category: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    operating_location: str
    max_budget_capacity: Optional[float] = None
    capabilities_description: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[float] = None
    current_status: Optional[str] = None
    max_budget_capacity: Optional[float] = None
    capabilities_description: Optional[str] = None

class VendorResponse(VendorBase):
    id: UUID
    rating: float
    current_status: str
    created_at: datetime
    documents: List[DocumentResponse] = [] # Includes nested documents

    model_config = ConfigDict(from_attributes=True)