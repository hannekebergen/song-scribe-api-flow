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
    try:
        # Get database URL
        database_url = get_database_url()
        logger.info(f"Using database: {database_url.split('@')[1] if '@' in database_url else 'local'}")
        
        # Test database connection
        if not test_database_connection(database_url):
            logger.error("Cannot proceed with migrations due to database connection issues")
            sys.exit(1)
        
        # Check current migration state
        check_migration_table(database_url)
        
        # Check if problematic column exists
        column_exists_before = check_persoonlijk_verhaal_column(database_url)
        
        # Set up Alembic configuration
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        logger.info("Starting database migrations...")
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Migrations completed successfully")
        
        # Check if column was added
        column_exists_after = check_persoonlijk_verhaal_column(database_url)
        
        if not column_exists_before and column_exists_after:
            logger.info("✅ persoonlijk_verhaal column was successfully added")
        elif column_exists_after:
            logger.info("✅ persoonlijk_verhaal column already exists")
        else:
            logger.warning("⚠️ persoonlijk_verhaal column still missing after migration")
            
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("=== Database Migration Script ===")
    success = run_migrations()
    if success:
        logger.info("=== Migration Script Completed Successfully ===")
        sys.exit(0)
    else:
        logger.error("=== Migration Script Failed ===")
        sys.exit(1)
