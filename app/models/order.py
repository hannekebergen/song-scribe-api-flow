"""
SQLAlchemy model voor Plug&Pay bestellingen.
"""

import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.exc import IntegrityError

from app.db.session import Base

# Configureer logging
logger = logging.getLogger(__name__)

class Order(Base):
    """
    SQLAlchemy model voor een Plug&Pay bestelling.
    """
    __tablename__ = "orders"
    
    # Primaire sleutel
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Bestelling details
    order_id = Column(String, unique=True, nullable=False, index=True)
    klant_naam = Column(String, nullable=False)
    klant_email = Column(String, nullable=False)
    product_naam = Column(String, nullable=False)
    bestel_datum = Column(DateTime, default=datetime.utcnow)
    
    # Voeg een unieke constraint toe op order_id
    __table_args__ = (
        UniqueConstraint('order_id', name='uix_order_id'),
    )
    
    def __repr__(self):
        """String representatie van het Order object."""
        return f"<Order(id={self.id}, order_id='{self.order_id}', klant='{self.klant_naam}')>"
    
    @classmethod
    def create_from_plugpay_data(cls, db_session, order_data):
        """
        Maakt een nieuw Order object aan op basis van Plug&Pay order data.
        
        Args:
            db_session: SQLAlchemy database sessie
            order_data (dict): Order data van de Plug&Pay API
            
        Returns:
            Order: Het aangemaakte of bestaande Order object
            bool: True als een nieuw object is aangemaakt, False als het al bestond
            
        Raises:
            ValueError: Als verplichte velden ontbreken in de order_data
        """
        try:
            # Controleer of de bestelling al bestaat
            existing_order = db_session.query(cls).filter_by(
                order_id=order_data.get("id")
            ).first()
            
            if existing_order:
                logger.info(f"Bestelling {order_data.get('id')} bestaat al in de database")
                return existing_order, False
            
            # Haal de benodigde velden op uit de order_data
            customer = order_data.get("customer", {})
            products = order_data.get("products", [])
            
            # Controleer of alle verplichte velden aanwezig zijn
            if not order_data.get("id"):
                raise ValueError("Bestelling heeft geen order_id")
            
            if not customer.get("name"):
                raise ValueError("Bestelling heeft geen klantnaam")
            
            # Maak een nieuw Order object aan
            new_order = cls(
                order_id=order_data.get("id"),
                klant_naam=customer.get("name", "Onbekend"),
                klant_email=customer.get("email", "onbekend@example.com"),
                product_naam=products[0].get("name", "Onbekend product") if products else "Onbekend product",
                bestel_datum=datetime.fromisoformat(order_data.get("created_at").replace("Z", "+00:00")) 
                            if order_data.get("created_at") else datetime.utcnow()
            )
            
            # Voeg het nieuwe object toe aan de database
            db_session.add(new_order)
            db_session.commit()
            
            logger.info(f"Nieuwe bestelling {new_order.order_id} toegevoegd aan de database")
            return new_order, True
            
        except IntegrityError as e:
            db_session.rollback()
            logger.error(f"Database integriteitsconflict bij toevoegen bestelling: {str(e)}")
            # Probeer de bestaande bestelling op te halen
            existing_order = db_session.query(cls).filter_by(
                order_id=order_data.get("id")
            ).first()
            return existing_order, False
            
        except Exception as e:
            db_session.rollback()
            logger.error(f"Fout bij aanmaken bestelling: {str(e)}")
            raise
