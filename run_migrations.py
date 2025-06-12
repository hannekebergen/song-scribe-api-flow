#!/usr/bin/env python
"""
Script om Alembic-migraties uit te voeren zonder afhankelijk te zijn van het console-script.
"""

from alembic.config import Config
from alembic import command
import os
import logging
import urllib.parse

# Laad .env
from dotenv import load_dotenv
load_dotenv()

# Configureer logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_migrations():
    """Voer alle Alembic-migraties uit (upgrade head)."""
    try:
        # Zorg dat we de juiste alembic.ini gebruiken
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        
        # Haal de DATABASE_URL op en zorg dat speciale tekens in het wachtwoord correct worden verwerkt
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            # Parse de URL en escape het wachtwoord indien nodig
            parts = db_url.split(":")
            if len(parts) >= 3 and "@" in db_url:
                # Format: postgresql://username:password@host:port/database
                prefix = parts[0] + ":" + parts[1] + ":"
                rest = db_url[len(prefix):]
                at_pos = rest.find("@")
                if at_pos > 0:
                    password = rest[:at_pos]
                    # Escape het wachtwoord als het speciale tekens bevat
                    password = urllib.parse.quote(password, safe="")
                    rest = rest[at_pos:]
                    db_url = prefix + password + rest
                    logger.info("Database URL aangepast voor speciale tekens in wachtwoord")
            
            # Escape % tekens voor configparser
            safe_db_url = db_url.replace("%", "%%")
            
            # Stel de database URL in voor Alembic
            alembic_cfg.set_main_option("sqlalchemy.url", safe_db_url)
            logger.info(f"Using database: {db_url.split('@')[1] if '@' in db_url else db_url}")
        
        # Voer de migratie uit
        command.upgrade(alembic_cfg, "head")
        
        print("✅ Alembic migrations applied successfully.")
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        raise

if __name__ == "__main__":
    run_migrations()
