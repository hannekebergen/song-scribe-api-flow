"""Merge thema system and origin_song_id branches

Revision ID: 33dc0231c81c
Revises: f1g2h3i4j5k6, add_thema_id_to_orders
Create Date: 2025-06-26 14:37:24.439674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33dc0231c81c'
down_revision = ('f1g2h3i4j5k6', 'add_thema_id_to_orders')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
