"""Add raw_data JSONB to orders

Revision ID: c3d4e5f6g7h8
Revises: b2c3d4e5f6g7
Create Date: 2025-06-12 16:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6g7h8'
down_revision: Union[str, None] = 'b2c3d4e5f6g7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add raw_data JSONB column to orders table
    op.add_column('orders', sa.Column('raw_data', JSONB, nullable=True))


def downgrade() -> None:
    # Remove raw_data column from orders table
    op.drop_column('orders', 'raw_data')
