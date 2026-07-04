from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date, datetime

# TODO: Currency and amount/value in minor unit
class WorkRequirementBase(BaseModel):
    title: str
    description: str
    category: str
    location: str
    estimated_value: float
    priority: Optional[str] = "Medium"
    expected_start_date: date

class WorkRequirementCreate(WorkRequirementBase):
    pass

class WorkRequirementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    estimated_value: Optional[float] = None
    priority: Optional[str] = None
    expected_start_date: Optional[date] = None
    status: Optional[str] = None

class WorkRequirementResponse(WorkRequirementBase):
    id: UUID
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)