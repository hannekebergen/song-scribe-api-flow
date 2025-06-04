#!/usr/bin/env python
"""
CLI script voor het uitvoeren van administratieve taken voor de Song Scribe API.
"""

import argparse
import logging
import sys
from dotenv import load_dotenv

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Laad environment variables
load_dotenv()

def setup_db():
    """Initialiseert de database tabellen."""
    from app.db.session import init_db
    
    logger.info("Database tabellen initialiseren...")
    init_db()
    logger.info("Database tabellen succesvol geïnitialiseerd")

def fetch_orders():
    """Haalt recente bestellingen op van Plug&Pay en slaat ze op in de database."""
    from app.db.session import SessionLocal
    from app.services.plugpay_client import fetch_and_store_recent_orders
    
    logger.info("Bestellingen ophalen van Plug&Pay API...")
    db = SessionLocal()
    try:
        added, skipped = fetch_and_store_recent_orders(db)
        logger.info(f"Resultaat: {added} nieuwe bestellingen toegevoegd, {skipped} overgeslagen")
    except Exception as e:
        logger.error(f"Fout bij ophalen van bestellingen: {str(e)}")
    finally:
        db.close()

def main():
    """Hoofdfunctie voor de CLI."""
    parser = argparse.ArgumentParser(description="Song Scribe API CLI")
    subparsers = parser.add_subparsers(dest="command", help="Beschikbare commando's")
    
    # Commando voor het initialiseren van de database
    subparsers.add_parser("init-db", help="Initialiseert de database tabellen")
    
    # Commando voor het ophalen van bestellingen
    subparsers.add_parser("fetch-orders", help="Haalt recente bestellingen op van Plug&Pay")
    
    args = parser.parse_args()
    
    if args.command == "init-db":
        setup_db()
    elif args.command == "fetch-orders":
        fetch_orders()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
