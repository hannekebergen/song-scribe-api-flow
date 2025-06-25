#!/usr/bin/env python3
"""
Refresh Orders - Verbeterde Data Ophaling

Dit script test en refresht orders met de nieuwe gecombineerde v1+v2 API aanpak.
"""

import os
import sys
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Voeg de app directory toe aan het pad
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models.order import Order
from app.services.plugpay_client import get_order_details, dump_safe_json

# Laad environment variables
load_dotenv()

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_improved_data_fetching():
    """Test de verbeterde data-ophaling met een sample order."""
    logger.info("🧪 Testen van verbeterde data-ophaling (v1+v2 API)...")
    
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Haal een sample order op
        order = db.query(Order).first()
        if not order:
            logger.error("Geen orders gevonden om te testen")
            return
        
        logger.info(f"🎯 Testen met order {order.order_id}")
        logger.info(f"📋 Huidige raw_data keys: {list(order.raw_data.keys()) if order.raw_data else 'None'}")
        
        # Test de nieuwe functie
        order_details = get_order_details(order.order_id)
        
        # Analyseer resultaten
        has_address = bool(order_details.get('address'))
        has_custom_fields = bool(order_details.get('custom_field_inputs') or order_details.get('custom_fields'))
        has_items = bool(order_details.get('items'))
        has_products = bool(order_details.get('products'))
        
        logger.info(f"\n📊 Nieuwe data resultaten:")
        logger.info(f"   🏠 Address data: {has_address}")
        logger.info(f"   📦 Custom fields: {has_custom_fields}")
        logger.info(f"   📋 Items: {has_items} ({len(order_details.get('items', []))} items)")
        logger.info(f"   🛍️ Products: {has_products} ({len(order_details.get('products', []))} products)")
        logger.info(f"   🔑 Total keys: {len(order_details.keys())}")
        
        if has_address:
            address = order_details['address']
            logger.info(f"\n👤 Address informatie:")
            logger.info(f"   - full_name: {address.get('full_name', 'N/A')}")
            logger.info(f"   - firstname: {address.get('firstname', 'N/A')}")
            logger.info(f"   - lastname: {address.get('lastname', 'N/A')}")
            logger.info(f"   - email: {address.get('email', 'N/A')}")
        
        if has_custom_fields:
            custom_fields = order_details.get('custom_field_inputs', [])
            logger.info(f"\n📝 Custom fields ({len(custom_fields)} total):")
            for i, field in enumerate(custom_fields[:5]):  # Show first 5
                logger.info(f"   {i+1}. {field.get('name', 'N/A')}: {field.get('value', 'N/A')}")
        
        # Test klantnaam extractie
        logger.info(f"\n🎯 Klantnaam extractie test:")
        
        # Simuleer de extractie logica
        klantnaam = None
        
        # Stap 1: Address
        if order_details.get('address', {}).get('full_name'):
            klantnaam = order_details['address']['full_name'].strip()
            logger.info(f"   ✅ Gevonden via address.full_name: '{klantnaam}'")
        elif order_details.get('address', {}).get('firstname'):
            firstname = order_details['address'].get('firstname', '').strip()
            lastname = order_details['address'].get('lastname', '').strip()
            if firstname and lastname:
                klantnaam = f"{firstname} {lastname}"
                logger.info(f"   ✅ Gevonden via address.firstname+lastname: '{klantnaam}'")
            elif firstname:
                klantnaam = firstname
                logger.info(f"   ✅ Gevonden via address.firstname: '{klantnaam}'")
        
        # Stap 2: Custom fields
        if not klantnaam:
            custom_fields = order_details.get('custom_field_inputs', [])
            name_fields = ['Voornaam', 'Voor wie is dit lied?', 'Voor wie', 'Naam', 'Klant naam']
            for field in custom_fields:
                field_name = field.get('name', '')
                field_value = field.get('value', '').strip()
                if field_name in name_fields and field_value:
                    klantnaam = field_value
                    logger.info(f"   ✅ Gevonden via custom field '{field_name}': '{klantnaam}'")
                    break
        
        if not klantnaam:
            logger.info(f"   ❌ Geen klantnaam gevonden")
        
        return order_details
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        return None
    finally:
        db.close()

def refresh_sample_orders(count=5):
    """Refresh een paar sample orders om de verbetering te testen."""
    logger.info(f"🔄 Refreshing {count} sample orders...")
    
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        orders = db.query(Order).limit(count).all()
        logger.info(f"📊 {len(orders)} orders gevonden om te refreshen")
        
        updated_count = 0
        address_count = 0
        custom_fields_count = 0
        
        for i, order in enumerate(orders, 1):
            try:
                logger.info(f"🔄 [{i}/{len(orders)}] Refreshing order {order.order_id}...")
                
                # Haal nieuwe gecombineerde details op
                order_details = get_order_details(order.order_id)
                
                # Update raw_data
                order.raw_data = json.loads(dump_safe_json(order_details))
                db.commit()
                
                # Analyseer verbetering
                has_address = bool(order.raw_data.get('address'))
                has_custom_fields = bool(order.raw_data.get('custom_field_inputs') or order.raw_data.get('custom_fields'))
                
                if has_address:
                    address_count += 1
                if has_custom_fields:
                    custom_fields_count += 1
                
                updated_count += 1
                logger.info(f"✅ Order {order.order_id} updated - Address: {has_address}, Custom fields: {has_custom_fields}")
                
            except Exception as e:
                logger.error(f"❌ Error updating order {order.order_id}: {e}")
        
        logger.info(f"\n🎉 Sample refresh resultaten:")
        logger.info(f"   ✅ {updated_count} orders updated")
        logger.info(f"   🏠 {address_count} orders hebben nu address data ({address_count/len(orders)*100:.1f}%)")
        logger.info(f"   📦 {custom_fields_count} orders hebben nu custom fields ({custom_fields_count/len(orders)*100:.1f}%)")
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    finally:
        db.close()

def main():
    """Hoofdfunctie."""
    logger.info("🚀 Refresh Orders - Verbeterde Data Ophaling Test")
    logger.info("=" * 60)
    
    # Stap 1: Test de nieuwe data-ophaling
    logger.info("STAP 1: Test nieuwe data-ophaling functie")
    test_improved_data_fetching()
    
    # Stap 2: Refresh een paar sample orders
    logger.info("\nSTAP 2: Refresh sample orders")
    refresh_sample_orders(3)
    
    logger.info("\n💡 Als de resultaten goed zijn, kun je alle orders refreshen met:")
    logger.info("   python -c \"from refresh_orders_improved import refresh_all_orders; refresh_all_orders()\"")

def refresh_all_orders():
    """Refresh alle orders - alleen aan te roepen als de test succesvol is."""
    logger.info("🔄 Refreshing ALLE orders met verbeterde data-ophaling...")
    
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        orders = db.query(Order).all()
        logger.info(f"📊 {len(orders)} orders gevonden om te refreshen")
        
        updated_count = 0
        error_count = 0
        address_count = 0
        custom_fields_count = 0
        
        for i, order in enumerate(orders, 1):
            try:
                logger.info(f"🔄 [{i}/{len(orders)}] Refreshing order {order.order_id}...")
                
                # Haal nieuwe gecombineerde details op
                order_details = get_order_details(order.order_id)
                
                # Update raw_data
                order.raw_data = json.loads(dump_safe_json(order_details))
                db.commit()
                
                # Analyseer verbetering
                has_address = bool(order.raw_data.get('address'))
                has_custom_fields = bool(order.raw_data.get('custom_field_inputs') or order.raw_data.get('custom_fields'))
                
                if has_address:
                    address_count += 1
                if has_custom_fields:
                    custom_fields_count += 1
                
                updated_count += 1
                
                if i % 5 == 0:  # Log elke 5 orders
                    logger.info(f"📊 Progress: {i}/{len(orders)} - Address: {address_count}, Custom: {custom_fields_count}")
                
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Error updating order {order.order_id}: {e}")
        
        logger.info(f"\n🎉 Alle orders refresh complete!")
        logger.info(f"   ✅ {updated_count} orders successfully updated")
        logger.info(f"   🏠 {address_count} orders now have address data ({address_count/len(orders)*100:.1f}%)")
        logger.info(f"   📦 {custom_fields_count} orders now have custom fields ({custom_fields_count/len(orders)*100:.1f}%)")
        logger.info(f"   ❌ {error_count} orders had errors")
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 