#!/usr/bin/env python3
"""Update Sample Orders met Verbeterde Data"""

import os
import sys
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Setup
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.models.order import Order
from app.services.plugpay_client import get_order_details, dump_safe_json

def update_sample_orders():
    """Update een paar sample orders met de nieuwe data."""
    logger.info("🔄 Updating sample orders met verbeterde data...")
    
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Haal 5 sample orders op
        orders = db.query(Order).limit(5).all()
        logger.info(f"📊 {len(orders)} sample orders gevonden")
        
        for i, order in enumerate(orders, 1):
            try:
                logger.info(f"\n🔄 [{i}/5] Updating order {order.order_id}...")
                
                # Oude status
                old_has_address = bool(order.raw_data.get('address')) if order.raw_data else False
                old_custom_count = len(order.raw_data.get('custom_field_inputs', [])) if order.raw_data else 0
                
                # Haal nieuwe data op
                order_details = get_order_details(order.order_id)
                
                # Update raw_data
                order.raw_data = json.loads(dump_safe_json(order_details))
                db.commit()
                
                # Nieuwe status
                new_has_address = bool(order.raw_data.get('address'))
                new_custom_count = len(order.raw_data.get('custom_field_inputs', []))
                
                logger.info(f"   📊 Address: {old_has_address} → {new_has_address}")
                logger.info(f"   📊 Custom fields: {old_custom_count} → {new_custom_count}")
                
                # Test klantnaam extractie
                klantnaam = extract_klantnaam(order.raw_data)
                logger.info(f"   👤 Klantnaam: '{klantnaam}'")
                
            except Exception as e:
                logger.error(f"❌ Error updating order {order.order_id}: {e}")
        
        logger.info(f"\n✅ Sample orders updated! Nu test je de API endpoint:")
        logger.info(f"curl -X POST https://jouwsong-api.onrender.com/orders/update-names \\")
        logger.info(f"     -H \"X-API-Key: jouwsong2025\"")
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    finally:
        db.close()

def extract_klantnaam(raw_data):
    """Test klantnaam extractie logica."""
    if not raw_data:
        return "Onbekend"
    
    # Stap 1: Address full_name
    if raw_data.get('address', {}).get('full_name'):
        return raw_data['address']['full_name'].strip()
    
    # Stap 2: Address firstname + lastname
    address = raw_data.get('address', {})
    firstname = address.get('firstname', '').strip()
    lastname = address.get('lastname', '').strip()
    if firstname and lastname:
        return f"{firstname} {lastname}"
    elif firstname:
        return firstname
    
    # Stap 3: Custom fields
    custom_fields = raw_data.get('custom_field_inputs', [])
    name_fields = ['Voornaam', 'Voor wie is dit lied?', 'Voor wie', 'Naam', 'Klant naam']
    for field in custom_fields:
        field_name = field.get('name', '')
        field_value = field.get('value', '').strip()
        if field_name in name_fields and field_value:
            return field_value
    
    return "Onbekend"

if __name__ == "__main__":
    update_sample_orders() 