#!/usr/bin/env python3
"""Check alembic version table"""

from app.db.session import engine
import sqlalchemy as sa

with engine.connect() as conn:
    result = conn.execute(sa.text('SELECT version_num FROM alembic_version'))
    version = result.fetchone()[0]
    print(f'Current alembic version: {version}') 