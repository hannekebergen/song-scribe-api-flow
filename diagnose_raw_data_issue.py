#!/usr/bin/env python3
"""
Diagnose Raw Data Issue

Dit script analyseert waarom veel orders geen of onvolledige raw_data hebben
en test verschillende manieren om meer data op te halen van Plug&Pay.
"""

import os
import sys
import logging
import json
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Voeg de app directory toe aan het pad
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.session import get_db
from app.models.order import Order
from app.services.plugpay_client import get_api_key, get_order_details, get_recent_orders

# Laad environment variables
load_dotenv()

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def analyze_database_orders():
    """Analyseer orders in de database om te zien welke raw_data hebben."""
    logger.info("🔍 Analyseren van orders in database...")
    
    # Database connectie
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL niet gevonden in environment variables")
        return
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Haal alle orders op
        orders = db.query(Order).all()
        logger.info(f"📊 Totaal {len(orders)} orders gevonden in database")
        
        # Analyseer raw_data status
        empty_raw_data = 0
        null_raw_data = 0
        has_raw_data = 0
        has_custom_fields = 0
        has_address = 0
        has_products = 0
        
        sample_orders = []
        
        for order in orders:
            if order.raw_data is None:
                null_raw_data += 1
            elif not order.raw_data or order.raw_data == {}:
                empty_raw_data += 1
            else:
                has_raw_data += 1
                
                # Analyseer inhoud van raw_data
                if order.raw_data.get('custom_field_inputs') or order.raw_data.get('custom_fields'):
                    has_custom_fields += 1
                if order.raw_data.get('address'):
                    has_address += 1
                if order.raw_data.get('products'):
                    has_products += 1
                
                # Bewaar een sample voor analyse
                if len(sample_orders) < 3:
                    sample_orders.append({
                        'order_id': order.order_id,
                        'raw_data_keys': list(order.raw_data.keys()) if order.raw_data else [],
                        'has_custom_fields': bool(order.raw_data.get('custom_field_inputs') or order.raw_data.get('custom_fields')),
                        'has_address': bool(order.raw_data.get('address')),
                        'has_products': bool(order.raw_data.get('products'))
                    })
        
        logger.info(f"📈 Database analyse resultaten:")
        logger.info(f"   ✅ Orders met raw_data: {has_raw_data}/{len(orders)} ({has_raw_data/len(orders)*100:.1f}%)")
        logger.info(f"   📦 Orders met custom fields: {has_custom_fields}/{len(orders)} ({has_custom_fields/len(orders)*100:.1f}%)")
        logger.info(f"   🏠 Orders met address: {has_address}/{len(orders)} ({has_address/len(orders)*100:.1f}%)")
        logger.info(f"   🛍️ Orders met products: {has_products}/{len(orders)} ({has_products/len(orders)*100:.1f}%)")
        logger.info(f"   ❌ Orders met lege raw_data: {empty_raw_data}")
        logger.info(f"   🚫 Orders met null raw_data: {null_raw_data}")
        
        # Toon sample orders
        if sample_orders:
            logger.info(f"\n📋 Sample orders met raw_data:")
            for sample in sample_orders:
                logger.info(f"   Order {sample['order_id']}: keys={sample['raw_data_keys']}")
        
        return orders, sample_orders
        
    except Exception as e:
        logger.error(f"❌ Fout bij database analyse: {e}")
        return [], []
    finally:
        db.close()

def test_plugpay_api_methods():
    """Test verschillende manieren om data op te halen van Plug&Pay API."""
    logger.info("🧪 Testen van Plug&Pay API methoden...")
    
    try:
        api_key = get_api_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # Test 1: v1/orders (summary)
        logger.info("📡 Test 1: v1/orders (summary)")
        response = requests.get("https://api.plugandpay.nl/v1/orders", headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', [])
            logger.info(f"   ✅ {len(orders)} orders opgehaald")
            
            if orders:
                first_order = orders[0]
                logger.info(f"   📋 Eerste order keys: {list(first_order.keys())}")
                logger.info(f"   🔍 Heeft custom_field_inputs: {'custom_field_inputs' in first_order}")
                logger.info(f"   🔍 Heeft address: {'address' in first_order}")
                
                # Test 2: v1/orders/{id} (detail)
                order_id = first_order['id']
                logger.info(f"\n📡 Test 2: v1/orders/{order_id} (detail)")
                detail_url = f"https://api.plugandpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products,address"
                detail_response = requests.get(detail_url, headers=headers, timeout=30)
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    logger.info(f"   ✅ Detail data opgehaald")
                    logger.info(f"   📋 Detail keys: {list(detail_data.keys())}")
                    logger.info(f"   🔍 Custom field inputs: {len(detail_data.get('custom_field_inputs', []))}")
                    logger.info(f"   🔍 Products: {len(detail_data.get('products', []))}")
                    logger.info(f"   🔍 Address: {'address' in detail_data}")
                else:
                    logger.error(f"   ❌ Detail request failed: {detail_response.status_code}")
                
                # Test 3: v2/orders/{id} (nieuwe API)
                logger.info(f"\n📡 Test 3: v2/orders/{order_id} (v2 API)")
                v2_headers = headers.copy()
                v2_headers["User-Agent"] = "CustomApiCall/2"
                v2_url = f"https://api.plugandpay.nl/v2/orders/{order_id}?include=custom_fields,items,products"
                v2_response = requests.get(v2_url, headers=v2_headers, timeout=30)
                
                if v2_response.status_code == 200:
                    v2_data = v2_response.json()
                    if 'data' in v2_data:
                        order_data = v2_data['data']
                        logger.info(f"   ✅ v2 API data opgehaald")
                        logger.info(f"   📋 v2 keys: {list(order_data.keys())}")
                        logger.info(f"   🔍 Custom fields: {len(order_data.get('custom_fields', []))}")
                        logger.info(f"   🔍 Items: {len(order_data.get('items', []))}")
                        logger.info(f"   🔍 Products: {len(order_data.get('products', []))}")
                        
                        # Analyseer items voor custom fields
                        if 'items' in order_data:
                            total_item_custom_fields = 0
                            for item in order_data['items']:
                                if 'custom_fields' in item:
                                    total_item_custom_fields += len(item['custom_fields'])
                            logger.info(f"   🔍 Total item custom fields: {total_item_custom_fields}")
                    else:
                        logger.error(f"   ❌ v2 API response missing 'data' key")
                else:
                    logger.error(f"   ❌ v2 API request failed: {v2_response.status_code}")
                    
        else:
            logger.error(f"❌ Orders summary request failed: {response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ Fout bij API testen: {e}")

def test_order_detail_function():
    """Test de get_order_details functie uit plugpay_client."""
    logger.info("🔧 Testen van get_order_details functie...")
    
    try:
        # Haal eerst een order ID op
        orders_response = get_recent_orders()
        orders = orders_response.get("data", [])
        
        if not orders:
            logger.error("❌ Geen orders gevonden om te testen")
            return
            
        order_id = orders[0]['id']
        logger.info(f"🎯 Testen met order ID: {order_id}")
        
        # Test get_order_details functie
        order_details = get_order_details(order_id)
        
        logger.info(f"✅ get_order_details succesvol uitgevoerd")
        logger.info(f"📋 Returned keys: {list(order_details.keys())}")
        logger.info(f"🔍 Custom field inputs: {len(order_details.get('custom_field_inputs', []))}")
        logger.info(f"🔍 Custom fields: {len(order_details.get('custom_fields', []))}")
        logger.info(f"🔍 Products: {len(order_details.get('products', []))}")
        logger.info(f"🔍 Address: {'address' in order_details}")
        
        # Bewaar sample voor analyse
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_details_sample_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(order_details, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"💾 Sample order details opgeslagen in {filename}")
        
    except Exception as e:
        logger.error(f"❌ Fout bij testen van get_order_details: {e}")

def main():
    """Hoofdfunctie voor diagnose."""
    logger.info("🚀 Diagnose Raw Data Issue")
    logger.info("=" * 50)
    
    # Stap 1: Analyseer database
    orders, samples = analyze_database_orders()
    
    # Stap 2: Test API methoden
    test_plugpay_api_methods()
    
    # Stap 3: Test order details functie
    test_order_detail_function()
    
    logger.info("\n🎯 Diagnose samenvatting:")
    logger.info("1. Database analyse uitgevoerd - zie percentages hierboven")
    logger.info("2. API methoden getest - zie resultaten hierboven")
    logger.info("3. Order details functie getest")
    logger.info("\n💡 Volgende stappen:")
    logger.info("- Bekijk de gegenereerde sample files")
    logger.info("- Voer fetch_and_store_recent_orders() uit om orders bij te werken")
    logger.info("- Test daarna opnieuw de klantnaam extractie")

if __name__ == "__main__":
    main() 