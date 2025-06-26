#!/usr/bin/env python3
"""
Script to run database migrations with proper error handling and logging.
This script can be used both locally and in production environments.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

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
        sys.exit(1)
    return database_url

def test_database_connection(database_url):
    """Test database connection before running migrations."""
    try:
        logger.info("Testing database connection...")
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Database connection successful")
        return True
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error testing database connection: {e}")
        return False

def check_migration_table(database_url):
    """Check if alembic_version table exists and show current version."""
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                );
            """))
            table_exists = result.fetchone()[0]
            
            if table_exists:
                # Get current version
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                current_version = result.fetchone()
                if current_version:
                    logger.info(f"Current database version: {current_version[0]}")
                else:
                    logger.info("Alembic version table exists but is empty")
            else:
                logger.info("Alembic version table does not exist (fresh database)")
                
    except Exception as e:
        logger.warning(f"Could not check migration table: {e}")

def check_persoonlijk_verhaal_column(database_url):
    """Check if the persoonlijk_verhaal column exists in the orders table."""
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'orders' 
                    AND column_name = 'persoonlijk_verhaal'
                );
            """))
            column_exists = result.fetchone()[0]
            logger.info(f"persoonlijk_verhaal column exists: {column_exists}")
            return column_exists
    except Exception as e:
        logger.error(f"Could not check persoonlijk_verhaal column: {e}")
        return False

def run_migrations():
    """Run Alembic migrations with proper error handling."""
    engine = None
    try:
        # Get database URL
        database_url = get_database_url()
        logger.info(f"Using database: {database_url.split('@')[1] if '@' in database_url else 'local'}")
        
        # Test database connection
        if not test_database_connection(database_url):
            logger.error("Cannot proceed with migrations due to database connection issues")
            return False
        
        # Check current migration state
        check_migration_table(database_url)
        
        # Check if problematic column exists
        column_exists_before = check_persoonlijk_verhaal_column(database_url)
        
        # Set up Alembic configuration
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        logger.info("Starting database migrations...")
        
        # Check for multiple heads and handle gracefully
        try:
            # Try to upgrade to head
            logger.info("Attempting to upgrade to head...")
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations completed successfully")
        except Exception as e:
            if "Multiple head revisions" in str(e):
                logger.warning("Multiple head revisions detected, trying to upgrade to latest merge...")
                # Try to find and upgrade to the merge revision
                try:
                    command.upgrade(alembic_cfg, "heads")
                    logger.info("Successfully upgraded to all heads")
                except Exception as e2:
                    logger.error(f"Failed to upgrade to heads: {e2}")
                    raise e2
            else:
                logger.error(f"Migration error: {e}")
                raise e
        
        # Force flush logs and ensure clean exit
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
        
        # Check if column was added
        column_exists_after = check_persoonlijk_verhaal_column(database_url)
        
        if not column_exists_before and column_exists_after:
            logger.info("✅ persoonlijk_verhaal column was successfully added")
        elif column_exists_after:
            logger.info("✅ persoonlijk_verhaal column already exists")
        else:
            logger.warning("⚠️ persoonlijk_verhaal column still missing after migration")
        
        # Final log flush before returning
        sys.stdout.flush()
        sys.stderr.flush()
        logger.info("Migration function completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False
    finally:
        # Ensure any database connections are properly closed
        if engine:
            try:
                engine.dispose()
                logger.info("Database engine disposed")
            except Exception as e:
                logger.warning(f"Error disposing engine: {e}")
        
        # Force cleanup of any remaining connections
        import gc
        gc.collect()

if __name__ == "__main__":
    logger.info("=== Database Migration Script ===")
    
    # Add timeout tracking
    import time
    start_time = time.time()
    timeout_seconds = 300  # 5 minutes
    
    try:
        success = run_migrations()
        
        # Check if we exceeded timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            logger.error(f"Migration script exceeded timeout of {timeout_seconds} seconds")
            sys.exit(1)
        
        if success:
            logger.info(f"=== Migration Script Completed Successfully in {elapsed_time:.1f}s ===")
            # Force final flush and explicit exit
            sys.stdout.flush()
            sys.stderr.flush()
            logger.info("Script exiting with code 0")
            sys.exit(0)
        else:
            logger.error("=== Migration Script Failed ===")
            sys.stdout.flush()
            sys.stderr.flush()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
