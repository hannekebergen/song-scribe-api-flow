"""
Database session management voor PostgreSQL via SQLAlchemy.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import logging

# Configure logging first
logger = logging.getLogger(__name__)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Haal de database URL op uit environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is niet geconfigureerd. Postgres-verbinding vereist.")
    raise ValueError("DATABASE_URL environment variable is niet geconfigureerd")

# Maak de SQLAlchemy engine aan
engine = create_engine(
    DATABASE_URL,
    # Voor PostgreSQL is het belangrijk om de juiste pool size te hebben
    pool_pre_ping=True,  # Controleert of de verbinding nog actief is
    echo=False  # Zet op True voor SQL query logging
)

# Maak een sessionmaker aan
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class voor SQLAlchemy modellen
Base = declarative_base()

def get_db():
    """
    Dependency functie voor FastAPI om een database sessie te krijgen.
    Zorgt voor het correct sluiten van de sessie na gebruik.
    
    Yields:
        SQLAlchemy Session: Een database sessie
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialiseert de database door alle tabellen aan te maken.
    """
    try:
        # Import alle modellen om ze te registreren bij de Base
        from app.models.order import Order  # noqa
        
        # Maak alle tabellen aan
        Base.metadata.create_all(bind=engine)
        logger.info("Database tabellen succesvol aangemaakt")
    except Exception as e:
        logger.error(f"Fout bij initialiseren van database: {str(e)}")
        raise
