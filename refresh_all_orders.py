#!/usr/bin/env python3
"""
Refresh All Orders Script

Dit script haalt alle orders opnieuw op van Plug&Pay met de verbeterde
get_order_details functie die v1 en v2 API data combineert voor complete informatie.
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

def refresh_all_orders():
    """Refresh alle orders met nieuwe gecombineerde data van Plug&Pay v1+v2 API."""
    logger.info("🔄 Refreshing alle orders met verbeterde data-ophaling...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL niet gevonden in environment variables")
        return
    
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
                
                # Haal nieuwe gecombineerde details op (v1 + v2 API)
                order_details = get_order_details(order.order_id)
                
                # Update raw_data met de nieuwe gecombineerde data
                order.raw_data = json.loads(dump_safe_json(order_details))
                db.commit()
                
                # Analyseer wat we hebben gekregen
                has_address = bool(order.raw_data.get('address'))
                has_custom_fields = bool(order.raw_data.get('custom_field_inputs') or order.raw_data.get('custom_fields'))
                
                if has_address:
                    address_count += 1
                if has_custom_fields:
                    custom_fields_count += 1
                
                updated_count += 1
                logger.info(f"✅ Order {order.order_id} updated - Address: {has_address}, Custom fields: {has_custom_fields}")
                
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Error updating order {order.order_id}: {e}")
        
        logger.info(f"\n🎉 Refresh complete!")
        logger.info(f"   ✅ {updated_count} orders successfully updated")
        logger.info(f"   🏠 {address_count} orders now have address data ({address_count/len(orders)*100:.1f}%)")
        logger.info(f"   📦 {custom_fields_count} orders now have custom fields ({custom_fields_count/len(orders)*100:.1f}%)")
        logger.info(f"   ❌ {error_count} orders had errors")
        
        if updated_count > 0:
            logger.info(f"\n💡 Nu kun je de klantnaam extractie opnieuw testen!")
            logger.info(f"   curl -X POST https://jouwsong-api.onrender.com/orders/update-names \\")
            logger.info(f"        -H \"X-API-Key: jouwsong2025\"")
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    finally:
        db.close()

def test_sample_order():
    """Test de verbeterde data-ophaling met een sample order."""
    logger.info("🧪 Testen van verbeterde data-ophaling...")
    
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
        
        # Test de nieuwe functie
        order_details = get_order_details(order.order_id)
        
        # Analyseer resultaten
        has_address = bool(order_details.get('address'))
        has_custom_fields = bool(order_details.get('custom_field_inputs') or order_details.get('custom_fields'))
        has_items = bool(order_details.get('items'))
        has_products = bool(order_details.get('products'))
        
        logger.info(f"📊 Test resultaten:")
        logger.info(f"   🏠 Address data: {has_address}")
        logger.info(f"   📦 Custom fields: {has_custom_fields}")
        logger.info(f"   📋 Items: {has_items} ({len(order_details.get('items', []))} items)")
        logger.info(f"   🛍️ Products: {has_products} ({len(order_details.get('products', []))} products)")
        
        if has_address:
            address = order_details['address']
            logger.info(f"   👤 Address full_name: {address.get('full_name', 'N/A')}")
            logger.info(f"   👤 Address firstname: {address.get('firstname', 'N/A')}")
            logger.info(f"   👤 Address lastname: {address.get('lastname', 'N/A')}")
        
        if has_custom_fields:
            custom_fields = order_details.get('custom_field_inputs', [])
            logger.info(f"   📝 Custom fields count: {len(custom_fields)}")
            for field in custom_fields[:3]:  # Show first 3
                logger.info(f"      - {field.get('name', 'N/A')}: {field.get('value', 'N/A')}")
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
    finally:
        db.close()

def main():
    """Hoofdfunctie."""
    logger.info("🚀 Refresh All Orders - Verbeterde Data Ophaling")
    logger.info("=" * 60)
    
    import argparse
    parser = argparse.ArgumentParser(description="Refresh orders met verbeterde data")
    parser.add_argument("--test", action="store_true", help="Test alleen met een sample order")
    parser.add_argument("--refresh", action="store_true", help="Refresh alle orders")
    
    args = parser.parse_args()
    
    if args.test:
        test_sample_order()
    elif args.refresh:
        refresh_all_orders()
    else:
        logger.info("Gebruik --test om te testen of --refresh om alle orders bij te werken")
        logger.info("Bijvoorbeeld:")
        logger.info("  python refresh_all_orders.py --test")
        logger.info("  python refresh_all_orders.py --refresh")

if __name__ == "__main__":
    main() 