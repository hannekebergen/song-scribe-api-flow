"""add_origin_song_id_to_orders

Revision ID: f1g2h3i4j5k6
Revises: b89338895eb8
Create Date: 2025-06-25 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1g2h3i4j5k6'
down_revision = 'd4e5f6g7h8i9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add origin_song_id column to link upsell orders to their original orders
    op.add_column('orders', sa.Column('origin_song_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraint to reference the original order
    op.create_foreign_key(
        'fk_orders_origin_song_id',
        'orders', 'orders',
        ['origin_song_id'], ['order_id']
    )
    
    # Add index for performance
    op.create_index('idx_orders_origin_song_id', 'orders', ['origin_song_id'])


def downgrade() -> None:
    # Remove index
    op.drop_index('idx_orders_origin_song_id', table_name='orders')
    
    # Remove foreign key constraint
    op.drop_constraint('fk_orders_origin_song_id', 'orders', type_='foreignkey')
    
    # Remove column
    op.drop_column('orders', 'origin_song_id') 