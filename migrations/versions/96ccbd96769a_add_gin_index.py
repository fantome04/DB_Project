"""add GIN index

Revision ID: 96ccbd96769a
Revises: b771f8530337
Create Date: 2024-12-31 14:53:24.046100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96ccbd96769a'
down_revision: Union[str, None] = 'b771f8530337'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("CREATE INDEX idx_driver_details_gin ON driver USING GIN ((details::text) gin_trgm_ops);")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_driver_details_gin;")
