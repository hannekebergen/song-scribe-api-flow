"""Fix rhyme_pairs column type

Revision ID: fix_rhyme_pairs_type
Revises: ac5c3189725c
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_rhyme_pairs_type'
down_revision = 'ac5c3189725c'
branch_labels = None
depends_on = None


def upgrade():
    # Change rhyme_pairs column from ARRAY(String) to JSON
    op.alter_column('thema_rhyme_sets', 'rhyme_pairs',
                    existing_type=postgresql.ARRAY(sa.String()),
                    type_=postgresql.JSON(),
                    existing_nullable=False)


def downgrade():
    # Revert back to ARRAY(String) - but this might cause issues with existing data
    op.alter_column('thema_rhyme_sets', 'rhyme_pairs',
                    existing_type=postgresql.JSON(),
                    type_=postgresql.ARRAY(sa.String()),
                    existing_nullable=False)