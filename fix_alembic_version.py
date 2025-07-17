from app.db.session import engine
import sqlalchemy as sa

def fix_alembic_version():
    """Fix the alembic version to point to a valid revision"""
    # We'll use the merge migration as it should be the most recent
    new_version = 'merge_songtekst_and_other_heads'
    
    with engine.connect() as conn:
        # Update the version
        conn.execute(sa.text(f"UPDATE alembic_version SET version_num = '{new_version}'"))
        conn.commit()
        
        # Verify the change
        result = conn.execute(sa.text('SELECT version_num FROM alembic_version'))
        version = result.fetchone()[0]
        print(f'Updated alembic version to: {version}')

if __name__ == "__main__":
    fix_alembic_version() 