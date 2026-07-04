from sqlalchemy import Column, String, Float, Date, Text
from app.models.base import AuditBase


class WorkRequirement(AuditBase):
    __tablename__ = "work_requirements"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    location = Column(String(100), nullable=False, index=True)

    estimated_value = Column(Float, nullable=False)
    priority = Column(String(50), default="Medium")  # Low, Medium, High
    expected_start_date = Column(Date, nullable=False)

    status = Column(String(50), default="Open")  # Open, Sourcing, Awarded, Closed