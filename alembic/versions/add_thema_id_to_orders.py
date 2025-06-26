"""Add thema_id foreign key to orders table

Revision ID: add_thema_id_to_orders
Revises: 20250127_120000_create_thema_database_basics
Create Date: 2025-01-27 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_thema_id_to_orders'
down_revision = '20250127_120000'
branch_labels = None
depends_on = None

def upgrade():
    """Add thema_id column to orders table with optional FK to themas"""
    import logging
    logger = logging.getLogger('alembic.runtime.migration')
    
    # Add thema_id column as nullable integer
    op.add_column('orders', sa.Column('thema_id', sa.Integer(), nullable=True))
    logger.info("✅ Added thema_id column to orders table")
    
    # Add foreign key constraint to themas table
    op.create_foreign_key(
        'fk_orders_thema_id',
        'orders', 'themas',
        ['thema_id'], ['id'],
        ondelete='SET NULL'  # If thema is deleted, set order thema_id to NULL
    )
    logger.info("✅ Created foreign key constraint to themas table")
    
    # Add index for performance
    op.create_index('idx_orders_thema_id', 'orders', ['thema_id'])
    logger.info("✅ Added performance index on thema_id")

def downgrade():
    """Remove thema_id column and constraints"""
    import logging
    logger = logging.getLogger('alembic.runtime.migration')
    
    # Drop index
    op.drop_index('idx_orders_thema_id', table_name='orders')
    
    # Drop foreign key constraint
    op.drop_constraint('fk_orders_thema_id', 'orders', type_='foreignkey')
    
    # Drop column
    op.drop_column('orders', 'thema_id')
    
    logger.info("✅ Removed thema_id column and constraints") 