"""
SQLAlchemy model voor Plug&Pay bestellingen.
"""

import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Text
from sqlalchemy.dialects.postgresql import JSONB
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
    order_id = Column(Integer, unique=True, nullable=False, index=True)
    klant_naam = Column(String, nullable=True)
    klant_email = Column(String, nullable=False)
    product_naam = Column(String, nullable=False)
    bestel_datum = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSONB, nullable=True)
    
    # Afgeleide velden uit custom fields
    thema = Column(String, nullable=True)
    toon = Column(String, nullable=True)
    structuur = Column(String, nullable=True)
    beschrijving = Column(String, nullable=True)
    deadline = Column(String, nullable=True)

    typeOrder = Column(String)  # New field for order type
    
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
            
            # Verwijderd: validatie op klantnaam (nu nullable)
            # if not customer.get("name"):
            #     raise ValueError("Bestelling heeft geen klantnaam")
            
            # Haal custom fields op als die aanwezig zijn
            custom = {}
            custom_field_inputs = order_data.get("custom_field_inputs", [])
            for field in custom_field_inputs:
                name = field.get("name") or field.get("label")
                value = field.get("value") or field.get("input")
                if name and value:
                    custom[name] = value
            
            # Helper functie om waarden uit custom fields te halen
            def pick(*keys):
                for k in keys:
                    if k in custom:
                        return custom[k]
                return None
            
            # Verbeterde klantnaam extractie met custom fields fallback
            def get_klant_naam():
                # Probeer eerst customer.name
                if customer.get("name"):
                    return customer.get("name")
                
                # Dan address.full_name
                address = order_data.get("address", {})
                if address.get("full_name"):
                    return address.get("full_name")
                
                # Dan firstname + lastname uit address
                if address.get("firstname"):
                    firstname = address.get("firstname")
                    lastname = address.get("lastname", "")
                    return f"{firstname} {lastname}".strip()
                
                # Dan custom fields voor voornaam
                voornaam = pick("Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam")
                if voornaam:
                    achternaam = pick("Achternaam", "Van")
                    if achternaam:
                        return f"{voornaam} {achternaam}"
                    return voornaam
                
                return None
            
            # Maak een nieuw Order object aan
            new_order = cls(
                order_id=order_data.get("id"),
                klant_naam=get_klant_naam(),  # Gebruik verbeterde functie
                klant_email=customer.get("email", "onbekend@example.com"),
                product_naam=products[0].get("name", "Onbekend product") if products else "Onbekend product",
                bestel_datum=datetime.fromisoformat(order_data.get("created_at").replace("Z", "+00:00")) 
                            if order_data.get("created_at") else datetime.utcnow(),
                raw_data=order_data,  # Sla de volledige Plug&Pay payload op
                thema=pick("Vertel over de gelegenheid", "Gewenste stijl", "Thema"),
                toon=pick("Toon", "Sfeer"),
                structuur=pick("Structuur", "Song structuur"),
                beschrijving=pick("Beschrijf"),
                deadline=products[0].get("title", "").replace("Songtekst - ", "") if products else None,
                typeOrder=pick("Type order")
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
