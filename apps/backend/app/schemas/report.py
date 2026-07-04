from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Confidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class VendorRisk(BaseModel):
    category: str = Field(..., description="Short label, e.g. 'budget', 'rating', 'capacity'")
    level: RiskLevel
    detail: str = Field(..., description="One-sentence explanation")


class VendorPick(BaseModel):
    vendor_id: str = Field(..., description="UUID of the vendor as a string")
    name: str
    score: float = Field(..., ge=0.0, le=100.0)
    justification: str = Field(..., description="Why this vendor was chosen or considered")
    risks: List[VendorRisk] = Field(default_factory=list)


class VendorReport(BaseModel):
    """Structured executive summary for a work requirement recommendation."""

    work_requirement_id: str
    headline: str = Field(..., description="One-line TL;DR for the ops team")
    executive_summary: str = Field(..., description="2–3 sentence overview")
    primary_recommendation: VendorPick
    alternatives: List[VendorPick] = Field(
        default_factory=list, description="Runner-up vendors, best first"
    )
    overall_risks: List[str] = Field(
        default_factory=list, description="Cross-cutting risks not tied to one vendor"
    )
    confidence: Confidence = Field(..., description="Confidence in the primary recommendation")


class VendorReportResponse(VendorReport):
    """Response wrapper — same shape for now, kept separate for future audit fields."""

    model_config = ConfigDict(from_attributes=True)


class VendorReportStatus(BaseModel):
    work_requirement_id: UUID
    status: str = Field(..., description="pending | completed | failed")
    report: Optional[VendorReport] = None
