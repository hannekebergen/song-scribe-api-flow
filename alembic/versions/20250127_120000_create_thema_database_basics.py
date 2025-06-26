"""Create basic thema database tables

Revision ID: f1a2b3c4d5e6
Revises: d4e5f6g7h8i9
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '20250127_120000'
down_revision = 'f1g2h3i4j5k6'
branch_labels = None
depends_on = None

def upgrade():
    # Themas (hoofd-tabel)
    op.create_table('themas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint('uq_themas_name', 'themas', ['name'])

    # Thema elementen (keywords, power phrases, etc.)
    op.create_table('thema_elements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('thema_id', sa.Integer(), nullable=False),
        sa.Column('element_type', sa.String(length=30), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('usage_context', sa.String(length=50), nullable=True),
        sa.Column('weight', sa.Integer(), nullable=False, default=1),
        sa.Column('suno_format', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['thema_id'], ['themas.id'], ondelete='CASCADE')
    )

    # Rijmwoorden sets
    op.create_table('thema_rhyme_sets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('thema_id', sa.Integer(), nullable=False),
        sa.Column('rhyme_pattern', sa.String(length=10), nullable=False),
        sa.Column('words', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('difficulty_level', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['thema_id'], ['themas.id'], ondelete='CASCADE')
    )

    # Indexes voor performance
    op.create_index('ix_thema_elements_thema_id', 'thema_elements', ['thema_id'])
    op.create_index('ix_thema_elements_type', 'thema_elements', ['element_type'])
    op.create_index('ix_thema_rhyme_sets_thema_id', 'thema_rhyme_sets', ['thema_id'])

def downgrade():
    op.drop_index('ix_thema_rhyme_sets_thema_id')
    op.drop_index('ix_thema_elements_type')
    op.drop_index('ix_thema_elements_thema_id')
    op.drop_table('thema_rhyme_sets')
    op.drop_table('thema_elements')
    op.drop_table('themas') 