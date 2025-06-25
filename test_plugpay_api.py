#!/usr/bin/env python3
"""
Test script voor Plug&Pay API om de exacte data structuur te analyseren
"""

import requests
import json
import sys
from datetime import datetime

# API configuratie
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2U2YmI3ZjA5Zjk5OTczM2U1ODI0MDVmYzc4MDU3M2FjN2E1MDRmMzkwYTlmMmI1Mzg4OGZjMzRiMzlmOTk4MjRmNDIyYzIxYjQzNDJlOWYiLCJpYXQiOjE3NDkwNDU4MzkuMjc4NDE2LCJuYmYiOjE3NDkwNDU4MzkuMjc4NDE3LCJleHAiOjQ5MDQ3MTk0MzkuMjY0MDA0LCJzdWIiOiI2MjcyNSIsInNjb3BlcyI6W119.ehEbbZqXNRLLxoY3EDPop8ZESuWm1jtUmeEZvsX0TuVzZJNeczOD14mSWay1p7sDcKdMcfYV9VO9ORY28P5rROX0PgOT1bcvzbjy5rxVPnv-KwLR-atKu0zX634ebcvolOMfZQVOmO_hRXCmrkXUPUCLvx9DpZyOH8C6xAFL44VpClUhKa9ngtUdCCbnAfh5M411NFcGHDjJprF3k398ISMKLvEyLqYJ7Bx7BuNMcxm7XO00vh1ZzogAD1rhmKM9koprTdFllcKdyetin5Pp-K_2Hics6JpuOWq902hvJPbjEMChwvFX_SeHFXqE10Uk5pLveEm1j6HLhy5tqWn_z5yz8i5Pasxcgk6-bAZBAnnc6vu5gDQG0NC78XxN96q0_hdzn_9f3hlk9KaZsP8Jjf5fYxl2vyPQT_xbQNZwWD0yjdo6Gk0QZfKUFaXhObxtHdpqBLYVHCxHHj9yOcCxyrfpR7HkuTTBEwqq4HyQ3wu5oBJ-JHa9pXSh4n9SIUQh344FeiS0E9Vg12hIqqrtKb6hUEHFDgw4Dbfr0XDOEacZIPigUO6v2iMkOILDrqxLWbXtfC9bpqlcotd0D3t8TKZE8LFqU-EPPRmJTtz3JopDN53zNtiJSRUzKw7MbZJzfoVvNbschrVu-wh2HmeC7ZxUqqoEnsFB4eF70g1RU9I"
BASE_URL = "https://api.plugandpay.nl/v1"

def test_api_connection():
    """Test de basis API verbinding"""
    print("🔌 Testing Plug&Pay API connection...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        # Test basis endpoint
        response = requests.get(f"{BASE_URL}/orders", headers=headers, timeout=30)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def analyze_order_structure(orders_data):
    """Analyseer de structuur van de orders data"""
    print("\n🔍 Analyzing order data structure...")
    
    if not orders_data:
        print("❌ No orders data to analyze")
        return
    
    # Check if it's paginated response
    if isinstance(orders_data, dict):
        if 'data' in orders_data:
            orders = orders_data['data']
            print(f"📊 Paginated response with {len(orders)} orders")
            if 'meta' in orders_data:
                print(f"📈 Pagination info: {orders_data['meta']}")
        else:
            orders = [orders_data]  # Single order
    else:
        orders = orders_data  # Direct array
    
    if not orders:
        print("❌ No orders found in response")
        return
    
    print(f"📋 Total orders found: {len(orders)}")
    
    # Analyze first order in detail
    first_order = orders[0]
    print(f"\n🔎 Analyzing first order (ID: {first_order.get('id', 'unknown')}):")
    print(f"📅 Created: {first_order.get('created_at', 'unknown')}")
    
    # Check main structure
    print("\n📋 Main order fields:")
    for key, value in first_order.items():
        if isinstance(value, (dict, list)):
            if isinstance(value, list):
                print(f"  {key}: [{len(value)} items]")
            else:
                print(f"  {key}: {{dict with {len(value)} keys}}")
        else:
            print(f"  {key}: {type(value).__name__} = {str(value)[:100]}")
    
    # Analyze customer info
    if 'customer' in first_order:
        print(f"\n👤 Customer info:")
        customer = first_order['customer']
        for key, value in customer.items():
            print(f"  customer.{key}: {value}")
    
    # Analyze address info
    if 'address' in first_order:
        print(f"\n🏠 Address info:")
        address = first_order['address']
        for key, value in address.items():
            print(f"  address.{key}: {value}")
    
    # Analyze products
    if 'products' in first_order:
        products = first_order['products']
        print(f"\n🛍️ Products ({len(products)} items):")
        for i, product in enumerate(products):
            print(f"  Product {i+1}:")
            print(f"    id: {product.get('id')}")
            print(f"    title: {product.get('title', product.get('name', 'N/A'))}")
            if 'pivot' in product:
                pivot = product['pivot']
                print(f"    pivot.type: {pivot.get('type')}")
                print(f"    pivot.quantity: {pivot.get('quantity')}")
                print(f"    pivot.price: {pivot.get('incl', pivot.get('excl'))}")
    
    # Analyze custom fields
    custom_fields_found = False
    for field_name in ['custom_field_inputs', 'custom_fields', 'fields']:
        if field_name in first_order:
            custom_fields = first_order[field_name]
            print(f"\n📝 Custom fields ({field_name}):")
            custom_fields_found = True
            
            if isinstance(custom_fields, list):
                for i, field in enumerate(custom_fields):
                    if isinstance(field, dict):
                        name = field.get('name') or field.get('label') or f"field_{i}"
                        value = field.get('value') or field.get('input') or 'N/A'
                        print(f"  {name}: {value}")
                    else:
                        print(f"  field_{i}: {field}")
            elif isinstance(custom_fields, dict):
                for key, value in custom_fields.items():
                    print(f"  {key}: {value}")
    
    if not custom_fields_found:
        print("\n📝 No custom fields found in standard locations")
        # Check for custom fields in products or other locations
        if 'products' in first_order:
            for i, product in enumerate(first_order['products']):
                if 'custom_fields' in product:
                    print(f"  Found custom fields in product {i+1}: {product['custom_fields']}")
    
    return orders

def save_sample_data(orders_data, filename="sample_plugpay_data.json"):
    """Sla sample data op voor analyse"""
    print(f"\n💾 Saving sample data to {filename}...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(orders_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Sample data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def main():
    """Main test function"""
    print("🚀 Plug&Pay API Analysis Tool")
    print("=" * 50)
    
    # Test API connection
    orders_data = test_api_connection()
    
    if orders_data:
        # Analyze structure
        orders = analyze_order_structure(orders_data)
        
        # Save sample data
        save_sample_data(orders_data)
        
        print("\n✅ Analysis complete!")
        print(f"📁 Check 'sample_plugpay_data.json' for full data structure")
        
        # Generate summary
        if isinstance(orders_data, dict) and 'data' in orders_data:
            total_orders = len(orders_data['data'])
        else:
            total_orders = len(orders_data) if isinstance(orders_data, list) else 1
            
        print(f"\n📊 Summary:")
        print(f"  - Total orders retrieved: {total_orders}")
        print(f"  - Analysis timestamp: {datetime.now().isoformat()}")
        print(f"  - API endpoint: {BASE_URL}/orders")
        
    else:
        print("\n❌ Could not retrieve or analyze orders data")
        print("Please check:")
        print("  1. API key validity")
        print("  2. Network connection")
        print("  3. Plug&Pay API status")

if __name__ == "__main__":
    main() 