from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import AuditBase
from app.models.vendor import Vendor


class VendorDocument(AuditBase):
    __tablename__ = "vendor_documents"

    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String(100), nullable=False)  # e.g., Tax, Insurance
    file_path = Column(String(500), nullable=False)

    expiry_date = Column(Date, nullable=True)
    verification_status = Column(String(50), default="Pending")  # Pending, Verified, Rejected

    # Relationship back to Vendor
    vendor = relationship("Vendor", back_populates="documents")