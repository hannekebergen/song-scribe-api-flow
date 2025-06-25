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
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return
    
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
            
            # Custom fields extractie
            custom = {}
            custom_field_inputs = order.raw_data.get("custom_field_inputs", [])
            for field in custom_field_inputs:
                name = field.get("name") or field.get("label")
                value = field.get("value") or field.get("input")
                if name and value:
                    custom[name] = value
            
            def pick(*keys):
                for k in keys:
                    if k in custom:
                        return custom[k]
                return None
            
            # Verbeterde klantnaam extractie
            def get_klant_naam():
                # Probeer eerst customer.name
                if customer.get("name"):
                    return customer.get("name")
                
                # Dan address.full_name
                address = order.raw_data.get("address", {})
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
            
            new_klant_naam = get_klant_naam()
            
            # Update als er een verbetering is
            if new_klant_naam and new_klant_naam != order.klant_naam:
                old_name = order.klant_naam or "None"
                order.klant_naam = new_klant_naam
                logger.info(f"Order {order.order_id}: Updated klant_naam from '{old_name}' to '{new_klant_naam}'")
                updated_count += 1
            
            # Update voornaam field for better frontend display
            voornaam = pick("Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam")
            if not voornaam:
                # Try address firstname
                address = order.raw_data.get("address", {})
                voornaam = address.get("firstname")
            
            if voornaam and voornaam != order.voornaam:
                old_voornaam = order.voornaam or "None"
                order.voornaam = voornaam
                logger.info(f"Order {order.order_id}: Updated voornaam from '{old_voornaam}' to '{voornaam}'")
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