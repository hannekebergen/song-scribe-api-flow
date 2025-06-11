"""Alter orders.order_id to Integer

Revision ID: a1b2c3d4e5f6
Revises: 
Create Date: 2025-06-11 16:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alter column order_id from VARCHAR to INTEGER using postgresql_using
    op.alter_column('orders', 'order_id',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Integer(),
                    postgresql_using='order_id::integer',
                    existing_nullable=False)


def downgrade() -> None:
    # Alter column order_id back from INTEGER to VARCHAR using postgresql_using
    op.alter_column('orders', 'order_id',
                    existing_type=sa.Integer(),
                    type_=sa.VARCHAR(),
                    postgresql_using='order_id::varchar',
                    existing_nullable=False)
