from sqlalchemy import Column, String, Float, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.models.base import AuditBase


class Vendor(AuditBase):
    __tablename__ = "vendors"

    name = Column(String(255), nullable=False, index=True)
    vendor_type = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False, index=True)

    # Stored as JSON string or plain text for MVP
    contact_email = Column(String(255), nullable=False, unique=True)
    contact_phone = Column(String(50), nullable=True)

    operating_location = Column(String(100), nullable=False, index=True)
    rating = Column(Float, default=0.0)
    current_status = Column(String(50), default="Active")  # Active, Inactive, Blacklisted

    max_budget_capacity = Column(Float, nullable=True)

    # AI/Semantic Search Field (768 dimensions is standard for Gemini)
    semantic_profile = Column(Vector(768), nullable=True)
    capabilities_description = Column(Text, nullable=True)  # Text used to generate the vector

    documents = relationship(
        "VendorDocument",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )