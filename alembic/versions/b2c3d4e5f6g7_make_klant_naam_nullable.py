"""Make klant_naam nullable

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-06-12 10:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make klant_naam column nullable
    op.alter_column(
        "orders", "klant_naam",
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    # Revert klant_naam column to non-nullable
    op.alter_column(
        "orders", "klant_naam",
        existing_type=sa.String(),
        nullable=False,
    )
