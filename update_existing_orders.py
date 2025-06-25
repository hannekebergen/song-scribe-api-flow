"""
Script om bestaande orders bij te werken met verbeterde naam extractie
"""

import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import models and database
from app.models.order import Order
from app.db.session import get_db

def update_order_names():
    """Update existing orders with improved name extraction"""
    
    # Use production database URL
    database_url = "postgresql://song_scribe_db_user:EHoXvsQYuo72p2mKNhcrbJZYmVOBzw8D@dpg-d10nt6i4d50c73b0doq0-a/song_scribe_db"
    
    logger.info(f"Connecting to database: {database_url.split('@')[1] if '@' in database_url else database_url}")
    
    try:
        # Create database connection
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get all orders
        orders = db.query(Order).all()
        logger.info(f"Found {len(orders)} orders to process")
        
        updated_count = 0
        
        for order in orders:
            if not order.raw_data:
                logger.warning(f"Order {order.order_id} has no raw_data, skipping")
                continue
            
            # Extract improved name using the new logic
            customer = order.raw_data.get("customer", {})
            
            # Custom fields extractie (try both locations)
            custom = {}
            
            # Check root level custom_field_inputs
            custom_field_inputs = order.raw_data.get("custom_field_inputs", [])
            for field in custom_field_inputs:
                name = field.get("name") or field.get("label")
                value = field.get("value") or field.get("input")
                if name and value:
                    custom[name] = value
            
            # Check products level custom_field_inputs
            products = order.raw_data.get("products", [])
            for product in products:
                product_custom_fields = product.get("custom_field_inputs", [])
                for field in product_custom_fields:
                    name = field.get("name") or field.get("label")
                    value = field.get("value") or field.get("input")
                    if name and value:
                        custom[name] = value
            
            def pick(*keys):
                for k in keys:
                    if k in custom:
                        return custom[k]
                return None
            
            # Verbeterde klantnaam extractie (6-staps systeem)
            def get_klant_naam():
                # Stap 1: Address full_name
                address = order.raw_data.get("address", {})
                if address.get("full_name"):
                    return address.get("full_name")
                
                # Stap 2: Address firstname + lastname
                if address.get("firstname"):
                    firstname = address.get("firstname")
                    lastname = address.get("lastname", "")
                    return f"{firstname} {lastname}".strip()
                
                # Stap 3: Customer name
                if customer.get("name"):
                    return customer.get("name")
                
                # Stap 4: Custom fields (uitgebreide lijst)
                name_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
                    "Voor wie is het lied?", "Wie is de ontvanger?", 
                    "Naam ontvanger", "Klant naam"
                ]
                for field_name in name_fields:
                    value = pick(field_name)
                    if value:
                        # Probeer ook achternaam toe te voegen
                        achternaam = pick("Achternaam", "Van")
                        if achternaam:
                            return f"{value} {achternaam}"
                        return value
                
                # Stap 5: Name extraction from description (basic regex)
                description = order.raw_data.get("description", "")
                if description:
                    import re
                    # Zoek naar patronen zoals "voor [naam]" of "aan [naam]"
                    patterns = [
                        r"voor\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
                        r"aan\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
                        r"van\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)"
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, description, re.IGNORECASE)
                        if match:
                            return match.group(1).strip()
                
                return None
            
            new_klant_naam = get_klant_naam()
            
            # Update als er een verbetering is
            if new_klant_naam and new_klant_naam != order.klant_naam:
                old_name = order.klant_naam or "None"
                order.klant_naam = new_klant_naam
                logger.info(f"Order {order.order_id}: Updated klant_naam from '{old_name}' to '{new_klant_naam}'")
                updated_count += 1
            
            # Update voornaam field for better frontend display (4-staps systeem)
            def get_voornaam():
                # Stap 1: Address firstname
                address = order.raw_data.get("address", {})
                if address.get("firstname"):
                    return address.get("firstname")
                
                # Stap 2: Custom fields (uitgebreide lijst)
                voornaam_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
                    "Voor wie is het lied?", "Wie is de ontvanger?", 
                    "Naam ontvanger"
                ]
                for field_name in voornaam_fields:
                    value = pick(field_name)
                    if value:
                        return value.split()[0]  # First word only for voornaam
                
                # Stap 3: Customer name (first word)
                if customer.get("name"):
                    return customer.get("name").split()[0]
                
                # Stap 4: Address full_name (first word)
                if address.get("full_name"):
                    return address.get("full_name").split()[0]
                
                return None
            
            new_voornaam = get_voornaam()
            
            if new_voornaam and new_voornaam != order.voornaam:
                old_voornaam = order.voornaam or "None"
                order.voornaam = new_voornaam
                logger.info(f"Order {order.order_id}: Updated voornaam from '{old_voornaam}' to '{new_voornaam}'")
                updated_count += 1
        
        # Commit changes
        if updated_count > 0:
            db.commit()
            logger.info(f"Successfully updated {updated_count} orders")
        else:
            logger.info("No orders needed updating")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Error updating orders: {str(e)}")
        if 'db' in locals():
            db.rollback()
            db.close()

if __name__ == "__main__":
    update_order_names() 