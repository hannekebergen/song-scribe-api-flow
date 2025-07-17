#!/usr/bin/env python3
"""
Direct SQL migration script that bypasses alembic entirely.
This prevents any FastAPI imports that could trigger server startup.
"""

import os
import sys
import logging
import time
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set")
        return None
    return database_url

def parse_database_url(database_url):
    """Parse DATABASE_URL into connection parameters."""
    # Format: postgresql://user:password@host:port/database
    if not database_url.startswith('postgresql://'):
        raise ValueError("DATABASE_URL must start with postgresql://")
    
    # Remove protocol
    url_parts = database_url[13:]  # Remove 'postgresql://'
    
    # Split user:password@host:port/database
    if '@' not in url_parts:
        raise ValueError("Invalid DATABASE_URL format")
    
    auth_part, host_part = url_parts.split('@', 1)
    user, password = auth_part.split(':', 1)
    
    if '/' not in host_part:
        raise ValueError("Invalid DATABASE_URL format")
    
    host_port, database = host_part.rsplit('/', 1)
    
    if ':' in host_port:
        host, port = host_port.split(':', 1)
        port = int(port)
    else:
        host = host_port
        port = 5432
    
    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }

def test_connection(conn_params):
    """Test database connection."""
    try:
        logger.info("Testing database connection...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def get_current_version(conn_params):
    """Get current alembic version."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if alembic_version table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alembic_version'
            );
        """)
        
        if cursor.fetchone()[0]:
            cursor.execute("SELECT version_num FROM alembic_version")
            result = cursor.fetchone()
            version = result[0] if result else None
        else:
            version = None
            
        cursor.close()
        conn.close()
        return version
    except Exception as e:
        logger.error(f"Error getting current version: {e}")
        return None

def update_alembic_version(conn_params, version):
    """Update alembic version table."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            );
        """)
        
        # Delete old version and insert new one
        cursor.execute("DELETE FROM alembic_version")
        cursor.execute("INSERT INTO alembic_version (version_num) VALUES (%s)", (version,))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Updated alembic version to: {version}")
        return True
    except Exception as e:
        logger.error(f"Error updating alembic version: {e}")
        return False

def run_thema_id_migration(conn_params):
    """Run the thema_id migration directly."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if thema_id column already exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'orders' 
                AND column_name = 'thema_id'
            );
        """)
        
        if cursor.fetchone()[0]:
            logger.info("thema_id column already exists, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        logger.info("Adding thema_id column to orders table...")
        
        # Add thema_id column
        cursor.execute("ALTER TABLE orders ADD COLUMN thema_id INTEGER")
        logger.info("✅ Added thema_id column")
        
        # Add foreign key constraint
        cursor.execute("""
            ALTER TABLE orders 
            ADD CONSTRAINT fk_orders_thema_id 
            FOREIGN KEY (thema_id) REFERENCES themas(id) 
            ON DELETE SET NULL
        """)
        logger.info("✅ Added foreign key constraint")
        
        # Add index
        cursor.execute("CREATE INDEX idx_orders_thema_id ON orders (thema_id)")
        logger.info("✅ Added performance index")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error running thema_id migration: {e}")
        return False

def run_origin_song_id_migration(conn_params):
    """Run the origin_song_id migration directly."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if origin_song_id column already exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'orders' 
                AND column_name = 'origin_song_id'
            );
        """)
        
        if cursor.fetchone()[0]:
            logger.info("origin_song_id column already exists, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        logger.info("Adding origin_song_id column to orders table...")
        
        # Add origin_song_id column
        cursor.execute("ALTER TABLE orders ADD COLUMN origin_song_id INTEGER")
        logger.info("✅ Added origin_song_id column")
        
        # Add foreign key constraint
        cursor.execute("""
            ALTER TABLE orders 
            ADD CONSTRAINT fk_orders_origin_song_id 
            FOREIGN KEY (origin_song_id) REFERENCES orders(order_id)
        """)
        logger.info("✅ Added foreign key constraint")
        
        # Add index
        cursor.execute("CREATE INDEX idx_orders_origin_song_id ON orders (origin_song_id)")
        logger.info("✅ Added performance index")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error running origin_song_id migration: {e}")
        return False

def run_professional_prompt_migration(conn_params):
    """Run the professional_prompt migration directly."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if professional_prompt column already exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'themas' 
                AND column_name = 'professional_prompt'
            );
        """)
        
        if cursor.fetchone()[0]:
            logger.info("professional_prompt column already exists, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        logger.info("Adding professional_prompt column to themas table...")
        
        # Add professional_prompt column
        cursor.execute("ALTER TABLE themas ADD COLUMN professional_prompt TEXT")
        logger.info("✅ Added professional_prompt column")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error running professional_prompt migration: {e}")
        return False

def run_thema_rhyme_sets_migration(conn_params):
    """Create thema_rhyme_sets table if it doesn't exist."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if thema_rhyme_sets table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'thema_rhyme_sets'
            );
        """)
        
        if cursor.fetchone()[0]:
            logger.info("thema_rhyme_sets table already exists, skipping creation")
            cursor.close()
            conn.close()
            return True
        
        logger.info("Creating thema_rhyme_sets table...")
        
        # Create thema_rhyme_sets table
        cursor.execute("""
            CREATE TABLE thema_rhyme_sets (
                id SERIAL PRIMARY KEY,
                thema_id INTEGER NOT NULL REFERENCES themas(id) ON DELETE CASCADE,
                rhyme_pattern VARCHAR(10) NOT NULL,
                rhyme_pairs JSON NOT NULL,
                difficulty_level VARCHAR(20) DEFAULT 'medium' NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
        """)
        
        # Add indexes
        cursor.execute("CREATE INDEX idx_thema_rhyme_sets_thema_id ON thema_rhyme_sets (thema_id)")
        cursor.execute("CREATE INDEX idx_thema_rhyme_sets_rhyme_pattern ON thema_rhyme_sets (rhyme_pattern)")
        
        logger.info("✅ Created thema_rhyme_sets table with indexes")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating thema_rhyme_sets table: {e}")
        return False

def run_rhyme_pairs_fix_migration(conn_params):
    """Fix the rhyme_pairs column type from ARRAY(ARRAY(String)) to JSON."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if thema_rhyme_sets table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'thema_rhyme_sets'
            );
        """)
        
        if not cursor.fetchone()[0]:
            logger.info("thema_rhyme_sets table doesn't exist, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        # Check current column type
        cursor.execute("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'thema_rhyme_sets' 
            AND column_name = 'rhyme_pairs'
        """)
        
        result = cursor.fetchone()
        if not result:
            logger.info("rhyme_pairs column doesn't exist, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        current_type = result[0]
        if current_type == 'json':
            logger.info("rhyme_pairs column is already JSON type, skipping migration")
            cursor.close()
            conn.close()
            return True
        
        logger.info(f"Converting rhyme_pairs column from {current_type} to JSON...")
        
        # Convert column type to JSON
        cursor.execute("ALTER TABLE thema_rhyme_sets ALTER COLUMN rhyme_pairs TYPE JSON USING rhyme_pairs::json")
        logger.info("✅ Converted rhyme_pairs column to JSON type")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error running rhyme_pairs fix migration: {e}")
        return False

def run_direct_migrations():
    """Run migrations directly without alembic."""
    start_time = time.time()
    
    try:
        # Get database URL
        database_url = get_database_url()
        if not database_url:
            logger.error("Cannot proceed without DATABASE_URL")
            return False
        
        # Parse connection parameters
        conn_params = parse_database_url(database_url)
        logger.info(f"Using database: {conn_params['host']}:{conn_params['port']}/{conn_params['database']}")
        
        # Test connection
        if not test_connection(conn_params):
            logger.error("Cannot proceed with migrations due to database connection issues")
            return False
        
        # Get current version
        current_version = get_current_version(conn_params)
        logger.info(f"Current database version: {current_version}")
        
        # Run migrations based on current state
        migrations_run = []
        
        if current_version in [None, '20250127_120000']:
            logger.info("Running thema_id migration...")
            if run_thema_id_migration(conn_params):
                migrations_run.append("thema_id")
            else:
                return False
        
        if current_version in [None, '20250127_120000', 'add_thema_id_to_orders', 'd4e5f6g7h8i9']:
            logger.info("Running origin_song_id migration...")
            if run_origin_song_id_migration(conn_params):
                migrations_run.append("origin_song_id")
            else:
                return False
        
        # Always run professional_prompt migration (it checks if column exists)
        logger.info("Running professional_prompt migration...")
        if run_professional_prompt_migration(conn_params):
            migrations_run.append("professional_prompt")
        else:
            return False
        
        # Always run thema_rhyme_sets table creation (it checks if table exists)
        logger.info("Running thema_rhyme_sets table creation...")
        if run_thema_rhyme_sets_migration(conn_params):
            migrations_run.append("thema_rhyme_sets_table")
        else:
            return False
        
        # Always run rhyme_pairs fix migration (it checks if needed)
        logger.info("Running rhyme_pairs fix migration...")
        if run_rhyme_pairs_fix_migration(conn_params):
            migrations_run.append("rhyme_pairs_fix")
        else:
            return False
        
        # Update to final version
        final_version = "fix_rhyme_pairs_type"
        if migrations_run:
            if not update_alembic_version(conn_params, final_version):
                return False
            logger.info(f"Completed migrations: {', '.join(migrations_run)}")
        else:
            logger.info("No migrations needed, database is up to date")
        
        elapsed_time = time.time() - start_time
        logger.info(f"Direct migrations completed in {elapsed_time:.1f} seconds")
        
        return True
        
    except Exception as e:
        logger.error(f"Direct migration failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("=== Direct Database Migration Script ===")
    
    # Set timeout
    timeout_seconds = 180  # 3 minutes
    start_time = time.time()
    
    try:
        success = run_direct_migrations()
        
        # Check timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            logger.error(f"Migration script exceeded timeout of {timeout_seconds} seconds")
            os._exit(1)
        
        if success:
            logger.info(f"=== Direct Migration Script Completed Successfully in {elapsed_time:.1f}s ===")
            sys.stdout.flush()
            sys.stderr.flush()
            logger.info("Script exiting with code 0")
            
            # Force immediate exit
            import os
            os._exit(0)
        else:
            logger.error("=== Direct Migration Script Failed ===")
            sys.stdout.flush()
            sys.stderr.flush()
            
            # Force immediate exit
            import os
            os._exit(1)
            
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        import os
        os._exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        sys.stdout.flush()
        sys.stderr.flush()
        import os
        os._exit(1) 