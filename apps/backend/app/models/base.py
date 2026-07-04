import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class AuditBase(Base):
    __abstract__ = True  # Tells SQLAlchemy not to create a table for this class

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = Column(String, nullable=True)  # Could be tied to a User ID later
    updated_by = Column(String, nullable=True)

    # Soft-delete marker. NULL = active row.
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Optimistic Locking
    version = Column(Integer, default=1, nullable=False)

    @declared_attr
    def __mapper_args__(cls):
        """Enables optimistic locking on all models inheriting this base."""
        return {
            "version_id_col": cls.version
        }