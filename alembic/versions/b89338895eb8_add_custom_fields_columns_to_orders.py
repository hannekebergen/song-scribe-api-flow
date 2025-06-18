"""add_custom_fields_columns_to_orders

Revision ID: b89338895eb8
Revises: c3d4e5f6g7h8
Create Date: 2025-06-18 12:17:49.513506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b89338895eb8'
down_revision = 'c3d4e5f6g7h8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns for custom fields to the orders table
    op.add_column('orders', sa.Column('thema', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('toon', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('structuur', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('beschrijving', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('deadline', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the custom fields columns from the orders table
    op.drop_column('orders', 'deadline')
    op.drop_column('orders', 'beschrijving')
    op.drop_column('orders', 'structuur')
    op.drop_column('orders', 'toon')
    op.drop_column('orders', 'thema')
