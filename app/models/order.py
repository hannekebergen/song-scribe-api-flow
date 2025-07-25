"""
SQLAlchemy model voor Plug&Pay bestellingen.
"""

import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

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
    voornaam = Column(String, nullable=True)
    klant_email = Column(String, nullable=False)
    product_naam = Column(String, nullable=False)
    bestel_datum = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSONB, nullable=True)
    
    # Afgeleide velden uit custom fields
    thema = Column(String, nullable=True)  # Legacy string field for backward compatibility
    thema_id = Column(Integer, ForeignKey('themas.id', ondelete='SET NULL'), nullable=True)  # New FK to themas table
    toon = Column(String, nullable=True)
    structuur = Column(String, nullable=True)
    beschrijving = Column(String, nullable=True)
    deadline = Column(String, nullable=True)

    typeOrder = Column(String)  # New field for order type
    origin_song_id = Column(Integer, nullable=True)  # For upsell orders, references the original order
    
    # Relationships
    thema_obj = relationship("Thema", foreign_keys=[thema_id], lazy="select")
    
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
            
            # Verbeterde klantnaam extractie - 6-staps systeem (gesynchroniseerd met schemas/order.py)
            def get_klant_naam():
                # Stap 1: address.full_name (hoogste prioriteit)
                address = order_data.get("address", {})
                if address.get("full_name") and address.get("full_name").strip():
                    return address.get("full_name").strip()
                
                # Stap 2: address.firstname + lastname
                if address.get("firstname") and address.get("firstname").strip():
                    firstname = address.get("firstname").strip()
                    lastname = address.get("lastname", "").strip()
                    if lastname:
                        return f"{firstname} {lastname}"
                    return firstname
                
                # Stap 3: customer.name
                if customer.get("name") and customer.get("name").strip():
                    return customer.get("name").strip()
                
                # Stap 4: custom fields (uitgebreide lijst)
                name_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam", 
                    "Voor wie is het lied?", "Wie is de ontvanger?", "Naam ontvanger", 
                    "Klant naam", "Achternaam", "Van"
                ]
                
                # Probeer voornaam + achternaam combinatie
                voornaam = None
                achternaam = None
                for field_name in name_fields:
                    field_value = pick(field_name)
                    if field_value and field_value.strip():
                        if field_name in ["Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam", "Voor wie is het lied?", "Wie is de ontvanger?", "Naam ontvanger"]:
                            if not voornaam:
                                voornaam = field_value.strip()
                        elif field_name in ["Achternaam", "Van"]:
                            if not achternaam:
                                achternaam = field_value.strip()
                
                if voornaam:
                    if achternaam:
                        return f"{voornaam} {achternaam}"
                    return voornaam
                
                # Stap 5: description parsing (eenvoudige versie voor performance)
                beschrijving = pick("Beschrijf")
                if beschrijving and len(beschrijving) > 10:
                    # Zoek naar patronen zoals "voor [naam]", "aan [naam]", etc.
                    import re
                    patterns = [
                        r'\bvoor\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b',
                        r'\baan\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b',
                        r'\b([A-Z][a-zA-Z]+)\s+heet\b',
                        r'\bheet\s+([A-Z][a-zA-Z]+)\b'
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, beschrijving, re.IGNORECASE)
                        if match:
                            name = match.group(1).strip()
                            if len(name) > 1 and not name.lower() in ['het', 'de', 'een', 'mijn', 'zijn', 'haar']:
                                return name
                
                # Stap 6: product title analysis (laatste redmiddel)
                if products:
                    product_title = products[0].get("title", "")
                    if "voor" in product_title.lower():
                        # Simpele extractie uit product titel
                        parts = product_title.lower().split("voor")
                        if len(parts) > 1 and len(parts[1].strip()) > 2:
                            potential_name = parts[1].strip().title()
                            if len(potential_name) < 30:  # Redelijke naam lengte
                                return potential_name
                
                return None
            
            # Verbeterde voornaam extractie - 4-staps systeem (gesynchroniseerd met schemas/order.py)
            def get_voornaam():
                # Stap 1: address.firstname
                address = order_data.get("address", {})
                if address.get("firstname") and address.get("firstname").strip():
                    return address.get("firstname").strip()
                
                # Stap 2: custom fields voor voornaam (uitgebreide lijst)
                voornaam_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
                    "Voor wie is het lied?", "Wie is de ontvanger?", "Naam ontvanger"
                ]
                for field_name in voornaam_fields:
                    field_value = pick(field_name)
                    if field_value and field_value.strip():
                        # Voor voornaam nemen we alleen het eerste woord
                        return field_value.strip().split()[0]
                
                # Stap 3: customer name (first word)
                if customer.get("name") and customer.get("name").strip():
                    return customer.get("name").strip().split()[0]
                
                # Stap 4: address full_name (first word)
                if address.get("full_name") and address.get("full_name").strip():
                    return address.get("full_name").strip().split()[0]
                
                return None
            
            # Detecteer of dit een UpSell order is
            is_upsell = False
            if products:
                for product in products:
                    pivot_type = product.get("pivot", {}).get("type")
                    if pivot_type == "upsell":
                        is_upsell = True
                        break
            
            # Extract thema string first
            thema_string = pick("Vertel over de gelegenheid", "Gewenste stijl", "Thema")
            
            # Try to find corresponding thema_id for the thema string
            thema_id = None
            if thema_string:
                try:
                    from app.services.thema_service import get_thema_service
                    thema_service = get_thema_service(db_session)
                    thema_id = thema_service.find_thema_id_for_string(thema_string)
                    if thema_id:
                        logger.info(f"Found thema_id {thema_id} for thema string '{thema_string}'")
                except Exception as e:
                    logger.warning(f"Could not find thema_id for '{thema_string}': {str(e)}")
            
            # Maak een nieuw Order object aan
            new_order = cls(
                order_id=order_data.get("id"),
                klant_naam=get_klant_naam(),  # Gebruik verbeterde functie
                voornaam=get_voornaam(),  # Nieuw voornaam veld
                klant_email=customer.get("email", "onbekend@example.com"),
                product_naam=products[0].get("name", "Onbekend product") if products else "Onbekend product",
                bestel_datum=datetime.fromisoformat(order_data.get("created_at").replace("Z", "+00:00")) 
                            if order_data.get("created_at") else datetime.utcnow(),
                raw_data=order_data,  # Sla de volledige Plug&Pay payload op
                thema=thema_string,  # Legacy string field
                thema_id=thema_id,  # New FK field
                toon=pick("Toon", "Sfeer"),
                structuur=pick("Structuur", "Song structuur"),
                beschrijving=pick("Beschrijf"),
                deadline=products[0].get("title", "").replace("Songtekst - ", "") if products else None,
                typeOrder=pick("Type order")
            )
            
            # Voor UpSell orders: probeer te linken aan originele order en neem thema over
            if is_upsell:
                from app.services.upsell_linking import find_original_order_for_upsell, inherit_theme_from_original
                
                original_order_id = find_original_order_for_upsell(db_session, order_data)
                if original_order_id:
                    new_order.origin_song_id = original_order_id
                    
                    # Als de UpSell order geen eigen thema heeft, neem het over van de originele order
                    if not new_order.thema or new_order.thema == '-':
                        inherit_theme_from_original(db_session, new_order, original_order_id)
            
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
