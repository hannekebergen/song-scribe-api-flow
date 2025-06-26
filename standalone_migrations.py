#!/usr/bin/env python3
"""
Standalone database migration script that doesn't import FastAPI code.
This prevents server startup conflicts during Render deployment.
"""

import os
import sys
import logging
import time
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
        return None
    return database_url

def test_database_connection(database_url):
    """Test database connection before running migrations."""
    try:
        logger.info("Testing database connection...")
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        engine.dispose()
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
    engine = None
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
    finally:
        if engine:
            engine.dispose()

def run_standalone_migrations():
    """Run Alembic migrations without importing FastAPI code."""
    start_time = time.time()
    
    try:
        # Get database URL
        database_url = get_database_url()
        if not database_url:
            logger.error("Cannot proceed without DATABASE_URL")
            return False
            
        logger.info(f"Using database: {database_url.split('@')[1] if '@' in database_url else 'local'}")
        
        # Test database connection
        if not test_database_connection(database_url):
            logger.error("Cannot proceed with migrations due to database connection issues")
            return False
        
        # Check current migration state
        check_migration_table(database_url)
        
        # Set up Alembic configuration using standalone config
        alembic_cfg = Config("alembic_standalone.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        logger.info("Starting database migrations...")
        logger.info("Attempting to upgrade to head...")
        
        # Run migrations
        try:
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations completed successfully")
        except Exception as e:
            if "Multiple head revisions" in str(e):
                logger.warning("Multiple head revisions detected, trying to upgrade to all heads...")
                try:
                    command.upgrade(alembic_cfg, "heads")
                    logger.info("Successfully upgraded to all heads")
                except Exception as e2:
                    logger.error(f"Failed to upgrade to heads: {e2}")
                    return False
            else:
                logger.error(f"Migration error: {e}")
                import traceback
                logger.error(f"Full traceback: {traceback.format_exc()}")
                return False
        
        elapsed_time = time.time() - start_time
        logger.info(f"Migration completed in {elapsed_time:.1f} seconds")
        
        # Force cleanup
        import gc
        gc.collect()
        
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("=== Standalone Database Migration Script ===")
    
    # Set timeout
    timeout_seconds = 300  # 5 minutes
    start_time = time.time()
    
    try:
        success = run_standalone_migrations()
        
        # Check timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            logger.error(f"Migration script exceeded timeout of {timeout_seconds} seconds")
            sys.exit(1)
        
        if success:
            logger.info(f"=== Migration Script Completed Successfully in {elapsed_time:.1f}s ===")
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