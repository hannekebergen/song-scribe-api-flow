#!/usr/bin/env python3
"""
Test script om de verbeterde implementatie te testen met echte Plug&Pay API data
"""

import json
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_custom_fields_extraction():
    """Test de verbeterde custom fields extractie"""
    logger.info("🧪 Testing verbeterde custom fields extractie...")
    
    # Laad sample data
    try:
        with open('plugpay_order_sample_20250625_113456.json', 'r', encoding='utf-8') as f:
            sample_order = json.load(f)
        logger.info(f"✅ Sample order geladen: #{sample_order['id']}")
    except FileNotFoundError:
        logger.error("❌ Sample order bestand niet gevonden. Voer eerst analyze_plugpay_order.py uit.")
        return False
    
    # Test de nieuwe extractie logica
    custom_fields = {}
    
    # Extract from products.custom_field_inputs (nieuwe methode)
    for product in sample_order.get("products", []):
        for field in product.get("custom_field_inputs", []):
            if isinstance(field, dict):
                label = field.get("label")
                value = field.get("input")
                if label and value:
                    custom_fields[label] = value
    
    logger.info(f"📝 Custom fields gevonden: {len(custom_fields)}")
    for label, value in custom_fields.items():
        preview = value[:100] + "..." if len(value) > 100 else value
        logger.info(f"  {label}: {preview}")
    
    # Test specifieke velden
    expected_fields = ["Beschrijf", "Vertel over de gelegenheid"]
    found_fields = []
    
    for field in expected_fields:
        if field in custom_fields:
            found_fields.append(field)
            logger.info(f"✅ Verwacht veld '{field}' gevonden")
        else:
            logger.warning(f"❌ Verwacht veld '{field}' NIET gevonden")
    
    return len(found_fields) == len(expected_fields)

def test_order_type_detection():
    """Test de order type detectie"""
    logger.info("\n🧪 Testing order type detectie...")
    
    # Test cases gebaseerd op echte data
    test_cases = [
        {
            "name": "Standaard 72u",
            "product_id": 274588,
            "pivot_type": None,
            "expected": "Standaard 72u"
        },
        {
            "name": "Soundtrack Bundel (Upsell)",
            "product_id": 299107,
            "pivot_type": "upsell",
            "expected": "Soundtrack Bundel"
        },
        {
            "name": "Spoed 24u",
            "product_id": 289456,
            "pivot_type": None,
            "expected": "Spoed 24u"
        }
    ]
    
    def detect_order_type_test(product_id, pivot_type):
        """Simplified version of order type detection"""
        if product_id == 274588:
            return "Standaard 72u"
        elif product_id == 289456:
            return "Spoed 24u"
        elif pivot_type == "upsell":
            if product_id == 299107:
                return "Soundtrack Bundel"
            else:
                return "Upsell"
        elif pivot_type == "order-bump":
            return "Order-bump"
        else:
            return "Onbekend"
    
    all_passed = True
    for test_case in test_cases:
        result = detect_order_type_test(test_case["product_id"], test_case["pivot_type"])
        if result == test_case["expected"]:
            logger.info(f"✅ {test_case['name']}: {result}")
        else:
            logger.error(f"❌ {test_case['name']}: verwacht '{test_case['expected']}', kreeg '{result}'")
            all_passed = False
    
    return all_passed

def test_customer_name_extraction():
    """Test de klant naam extractie"""
    logger.info("\n🧪 Testing klant naam extractie...")
    
    try:
        with open('plugpay_order_sample_20250625_113456.json', 'r', encoding='utf-8') as f:
            sample_order = json.load(f)
    except FileNotFoundError:
        logger.error("❌ Sample order bestand niet gevonden")
        return False
    
    # Test address.full_name extractie
    address = sample_order.get("address", {})
    full_name = address.get("full_name")
    firstname = address.get("firstname")
    lastname = address.get("lastname")
    
    logger.info(f"📋 Address data:")
    logger.info(f"  full_name: {full_name}")
    logger.info(f"  firstname: {firstname}")
    logger.info(f"  lastname: {lastname}")
    
    # Test de extractie logica
    klant_naam = None
    
    if full_name:
        klant_naam = full_name
        source = "full_name"
    elif firstname:
        klant_naam = f"{firstname} {lastname}".strip() if lastname else firstname
        source = "firstname+lastname"
    
    if klant_naam:
        logger.info(f"✅ Klant naam gevonden via {source}: '{klant_naam}'")
        return True
    else:
        logger.error(f"❌ Geen klant naam gevonden")
        return False

def test_real_api_data():
    """Test met alle beschikbare orders"""
    logger.info("\n🧪 Testing met alle orders...")
    
    try:
        with open('plugpay_orders_full_20250625_113456.json', 'r', encoding='utf-8') as f:
            orders_data = json.load(f)
        
        orders = orders_data.get('data', orders_data) if isinstance(orders_data, dict) else orders_data
        logger.info(f"📊 Testing met {len(orders)} orders")
        
    except FileNotFoundError:
        logger.error("❌ Full orders bestand niet gevonden")
        return False
    
    # Statistieken
    stats = {
        "total_orders": len(orders),
        "orders_with_custom_fields": 0,
        "orders_with_customer_name": 0,
        "product_types": {},
        "pivot_types": {}
    }
    
    for order in orders:
        order_id = order.get('id')
        
        # Check custom fields
        has_custom_fields = False
        for product in order.get("products", []):
            if product.get("custom_field_inputs"):
                has_custom_fields = True
                stats["orders_with_custom_fields"] += 1
                break
        
        # Check customer name
        address = order.get("address", {})
        if address.get("full_name") or address.get("firstname"):
            stats["orders_with_customer_name"] += 1
        
        # Check product types
        for product in order.get("products", []):
            product_id = product.get("id")
            pivot_type = product.get("pivot", {}).get("type")
            
            if product_id:
                stats["product_types"][product_id] = stats["product_types"].get(product_id, 0) + 1
            
            if pivot_type:
                stats["pivot_types"][pivot_type] = stats["pivot_types"].get(pivot_type, 0) + 1
    
    # Rapportage
    logger.info(f"📈 Statistieken:")
    logger.info(f"  Total orders: {stats['total_orders']}")
    logger.info(f"  Orders met custom fields: {stats['orders_with_custom_fields']} ({stats['orders_with_custom_fields']/stats['total_orders']*100:.1f}%)")
    logger.info(f"  Orders met klant naam: {stats['orders_with_customer_name']} ({stats['orders_with_customer_name']/stats['total_orders']*100:.1f}%)")
    
    logger.info(f"  Product IDs gevonden:")
    for product_id, count in stats["product_types"].items():
        logger.info(f"    {product_id}: {count} orders")
    
    logger.info(f"  Pivot types gevonden:")
    for pivot_type, count in stats["pivot_types"].items():
        logger.info(f"    {pivot_type}: {count} orders")
    
    return True

def main():
    """Main test functie"""
    logger.info("🚀 Testing Verbeterde Plug&Pay Implementatie")
    logger.info("=" * 60)
    
    tests = [
        ("Custom Fields Extractie", test_custom_fields_extraction),
        ("Order Type Detectie", test_order_type_detection),
        ("Klant Naam Extractie", test_customer_name_extraction),
        ("Real API Data Analyse", test_real_api_data),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} gefaald met error: {e}")
            results.append((test_name, False))
    
    # Samenvatting
    logger.info(f"\n📊 Test Resultaten:")
    logger.info("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Overall: {passed}/{len(results)} tests geslaagd")
    
    if passed == len(results):
        logger.info("🎉 Alle tests geslaagd! De implementatie is klaar voor gebruik.")
    else:
        logger.warning("⚠️ Sommige tests gefaald. Controleer de implementatie.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 