"""
Script to directly fetch and analyze orders from Plug&Pay API
This bypasses the database and focuses on the raw API data
"""

import os
import sys
import logging
import json
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("plugpay_analysis")

# Your API key
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2U2YmI3ZjA5Zjk5OTczM2U1ODI0MDVmYzc4MDU3M2FjN2E1MDRmMzkwYTlmMmI1Mzg4OGZjMzRiMzlmOTk4MjRmNDIyYzIxYjQzNDJlOWYiLCJpYXQiOjE3NDkwNDU4MzkuMjc4NDE2LCJuYmYiOjE3NDkwNDU4MzkuMjc4NDE3LCJleHAiOjQ5MDQ3MTk0MzkuMjY0MDA0LCJzdWIiOiI2MjcyNSIsInNjb3BlcyI6W119.ehEbbZqXNRLLxoY3EDPop8ZESuWm1jtUmeEZvsX0TuVzZJNeczOD14mSWay1p7sDcKdMcfYV9VO9ORY28P5rROX0PgOT1bcvzbjy5rxVPnv-KwLR-atKu0zX634ebcvolOMfZQVOmO_hRXCmrkXUPUCLvx9DpZyOH8C6xAFL44VpClUhKa9ngtUdCCbnAfh5M411NFcGHDjJprF3k398ISMKLvEyLqYJ7Bx7BuNMcxm7XO00vh1ZzogAD1rhmKM9koprTdFllcKdyetin5Pp-K_2Hics6JpuOWq902hvJPbjEMChwvFX_SeHFXqE10Uk5pLveEm1j6HLhy5tqWn_z5yz8i5Pasxcgk6-bAZBAnnc6vu5gDQG0NC78XxN96q0_hdzn_9f3hlk9KaZsP8Jjf5fYxl2vyPQT_xbQNZwWD0yjdo6Gk0QZfKUFaXhObxtHdpqBLYVHCxHHj9yOcCxyrfpR7HkuTTBEwqq4HyQ3wu5oBJ-JHa9pXSh4n9SIUQh344FeiS0E9Vg12hIqqrtKb6hUEHFDgw4Dbfr0XDOEacZIPigUO6v2iMkOILDrqxLWbXtfC9bpqlcotd0D3t8TKZE8LFqU-EPPRmJTtz3JopDN53zNtiJSRUzKw7MbZJzfoVvNbschrVu-wh2HmeC7ZxUqqoEnsFB4eF70g1RU9I"

def fetch_orders():
    """Fetch orders from Plug&Pay API"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    
    logger.info("🔌 Fetching orders from Plug&Pay API...")
    
    try:
        response = requests.get('https://api.plugandpay.nl/v1/orders', headers=headers, timeout=30)
        logger.info(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', [])
            logger.info(f"✅ Successfully fetched {len(orders)} orders")
            return orders
        else:
            logger.error(f"❌ API Error {response.status_code}: {response.text[:200]}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return None

def analyze_order_structure(order):
    """Analyze the structure of a single order"""
    logger.info(f"\n🔍 Analyzing Order #{order.get('id')}")
    logger.info(f"📅 Created: {order.get('created_at')}")
    
    # Main fields
    logger.info(f"📋 Main fields: {list(order.keys())}")
    
    # Customer info
    if 'customer' in order:
        customer = order['customer']
        logger.info(f"👤 Customer: {customer.get('name', 'N/A')} ({customer.get('email', 'N/A')})")
    
    # Address info
    if 'address' in order:
        address = order['address']
        logger.info(f"🏠 Address fields: {list(address.keys())}")
        if address.get('full_name'):
            logger.info(f"   full_name: {address['full_name']}")
        if address.get('firstname'):
            logger.info(f"   firstname: {address['firstname']}")
        if address.get('lastname'):
            logger.info(f"   lastname: {address['lastname']}")
    
    # Products
    if 'products' in order:
        products = order['products']
        logger.info(f"🛍️ Products ({len(products)} items):")
        for i, product in enumerate(products):
            logger.info(f"   {i+1}. ID: {product.get('id')} - {product.get('title', product.get('name', 'N/A'))}")
            if 'pivot' in product:
                pivot = product['pivot']
                logger.info(f"      pivot.type: {pivot.get('type')}")
                logger.info(f"      pivot.quantity: {pivot.get('quantity')}")
    
    # Custom fields analysis
    custom_fields_locations = []
    
    # Check root level
    for field_name in ['custom_field_inputs', 'custom_fields', 'fields']:
        if field_name in order:
            fields = order[field_name]
            custom_fields_locations.append(f"root.{field_name}")
            logger.info(f"📝 Found {field_name} at root level: {len(fields) if isinstance(fields, list) else 'dict'}")
            
            if isinstance(fields, list) and fields:
                logger.info(f"   Sample field: {fields[0]}")
            elif isinstance(fields, dict) and fields:
                sample_key = list(fields.keys())[0]
                logger.info(f"   Sample field: {sample_key} = {fields[sample_key]}")
    
    # Check in products
    if 'products' in order:
        for i, product in enumerate(order['products']):
            for field_name in ['custom_field_inputs', 'custom_fields', 'fields']:
                if field_name in product:
                    fields = product[field_name]
                    custom_fields_locations.append(f"products[{i}].{field_name}")
                    logger.info(f"📝 Found {field_name} in product {i+1}: {len(fields) if isinstance(fields, list) else 'dict'}")
    
    if not custom_fields_locations:
        logger.info("📝 No custom fields found in standard locations")
    else:
        logger.info(f"📝 Custom fields found in: {', '.join(custom_fields_locations)}")
    
    return order

def main():
    """Main analysis function"""
    logger.info("🚀 Plug&Pay API Data Analysis")
    logger.info("=" * 50)
    
    # Fetch orders
    orders = fetch_orders()
    
    if not orders:
        logger.error("❌ Could not fetch orders. Exiting.")
        return
    
    # Analyze first few orders
    analyze_count = min(3, len(orders))
    logger.info(f"\n📊 Analyzing first {analyze_count} orders out of {len(orders)} total")
    
    analyzed_orders = []
    for i in range(analyze_count):
        order = orders[i]
        analyzed_order = analyze_order_structure(order)
        analyzed_orders.append(analyzed_order)
    
    # Save sample data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save full data
    filename_full = f"plugpay_orders_full_{timestamp}.json"
    with open(filename_full, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"💾 Full orders data saved to {filename_full}")
    
    # Save sample of first order
    if orders:
        filename_sample = f"plugpay_order_sample_{timestamp}.json"
        with open(filename_sample, 'w', encoding='utf-8') as f:
            json.dump(orders[0], f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"💾 Sample order saved to {filename_sample}")
    
    # Summary
    logger.info(f"\n📊 Analysis Summary:")
    logger.info(f"   Total orders fetched: {len(orders)}")
    logger.info(f"   Orders analyzed: {analyze_count}")
    logger.info(f"   Timestamp: {datetime.now().isoformat()}")
    
    logger.info(f"\n✅ Analysis complete! Check the generated JSON files for detailed data structure.")

if __name__ == "__main__":
    main()
