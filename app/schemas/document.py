from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class DocumentResponse(BaseModel):
    id: UUID
    vendor_id: UUID
    document_type: str
    file_path: str
    expiry_date: Optional[date] = None
    verification_status: str
    created_at: datetime

    # DB model -> Python model
    model_config = ConfigDict(from_attributes=True)