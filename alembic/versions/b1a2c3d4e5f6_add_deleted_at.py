"""Add deleted_at column for soft deletes

Revision ID: b1a2c3d4e5f6
Revises: 4a0f7d7e0e28
Create Date: 2026-07-04 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b1a2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "4a0f7d7e0e28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLES = ("vendors", "work_requirements", "vendor_documents")


def upgrade() -> None:
    for table in TABLES:
        op.add_column(
            table,
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        )
        op.create_index(
            op.f(f"ix_{table}_deleted_at"), table, ["deleted_at"], unique=False
        )


def downgrade() -> None:
    for table in TABLES:
        op.drop_index(op.f(f"ix_{table}_deleted_at"), table_name=table)
        op.drop_column(table, "deleted_at")
