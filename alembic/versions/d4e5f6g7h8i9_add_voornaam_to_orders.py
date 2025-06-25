"""Add voornaam to orders

Revision ID: d4e5f6g7h8i9
Revises: ac5c3189725c
Create Date: 2025-06-25 13:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6g7h8i9'
down_revision: Union[str, None] = 'ac5c3189725c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add voornaam column to orders table
    op.add_column('orders', sa.Column('voornaam', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove voornaam column from orders table
    op.drop_column('orders', 'voornaam') 