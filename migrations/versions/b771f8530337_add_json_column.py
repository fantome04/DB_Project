"""add JSON column

Revision ID: b771f8530337
Revises: 21ce4ccab026
Create Date: 2024-12-31 14:40:14.695786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b771f8530337'
down_revision: Union[str, None] = '21ce4ccab026'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('driver', sa.Column('details', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('driver', 'details')
