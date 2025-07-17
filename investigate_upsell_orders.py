#!/usr/bin/env python3
"""
Script om UpSell orders te onderzoeken en te zien waarom ze niet gelinkt worden.
"""

import requests
import logging
from datetime import datetime

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def investigate_upsell_orders():
    """Onderzoek UpSell orders en waarom ze niet gelinkt worden."""
    
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("🔍 Investigating UpSell orders...")
        
        # Haal alle orders op
        response = requests.get(f"{BASE_URL}/orders/orders", headers=headers)
        
        if response.status_code != 200:
            logger.error(f"❌ Could not fetch orders: {response.status_code}")
            return
        
        orders = response.json()
        logger.info(f"📋 Found {len(orders)} total orders")
        
        # Categoriseer orders
        original_orders = []
        upsell_orders = []
        other_orders = []
        
        for order in orders:
            order_id = order.get('order_id')
            raw_data = order.get('raw_data', {})
            products = raw_data.get('products', [])
            
            is_upsell = False
            for product in products:
                pivot_type = product.get('pivot', {}).get('type')
                if pivot_type == "upsell":
                    is_upsell = True
                    break
            
            if is_upsell:
                upsell_orders.append(order)
            elif products and any(p.get('id') in [274588, 289456] for p in products):
                original_orders.append(order)
            else:
                other_orders.append(order)
        
        logger.info(f"📊 Order breakdown:")
        logger.info(f"   Original orders: {len(original_orders)}")
        logger.info(f"   UpSell orders: {len(upsell_orders)}")
        logger.info(f"   Other orders: {len(other_orders)}")
        
        # Analyseer UpSell orders
        if upsell_orders:
            logger.info("\n🔍 UpSell orders analysis:")
            for order in upsell_orders[:5]:  # Toon eerste 5
                order_id = order.get('order_id')
                klant_naam = order.get('klant_naam', 'Unknown')
                origin_song_id = order.get('origin_song_id')
                bestel_datum = order.get('bestel_datum')
                
                logger.info(f"   Order #{order_id}:")
                logger.info(f"     Klant: {klant_naam}")
                logger.info(f"     Origin song ID: {origin_song_id}")
                logger.info(f"     Bestel datum: {bestel_datum}")
                
                # Check raw_data voor customer info
                raw_data = order.get('raw_data', {})
                customer = raw_data.get('customer', {})
                address = raw_data.get('address', {})
                
                logger.info(f"     Customer email: {customer.get('email', 'None')}")
                logger.info(f"     Address full_name: {address.get('full_name', 'None')}")
                logger.info(f"     Address firstname: {address.get('firstname', 'None')}")
                logger.info("")
        else:
            logger.info("❌ No UpSell orders found!")
        
        # Analyseer originele orders
        if original_orders:
            logger.info("\n🔍 Original orders analysis:")
            for order in original_orders[:3]:  # Toon eerste 3
                order_id = order.get('order_id')
                klant_naam = order.get('klant_naam', 'Unknown')
                bestel_datum = order.get('bestel_datum')
                
                logger.info(f"   Order #{order_id}:")
                logger.info(f"     Klant: {klant_naam}")
                logger.info(f"     Bestel datum: {bestel_datum}")
                
                # Check raw_data voor customer info
                raw_data = order.get('raw_data', {})
                customer = raw_data.get('customer', {})
                address = raw_data.get('address', {})
                
                logger.info(f"     Customer email: {customer.get('email', 'None')}")
                logger.info(f"     Address full_name: {address.get('full_name', 'None')}")
                logger.info("")
        
        # Zoek specifiek naar order #13275510
        target_order = None
        for order in orders:
            if order.get('order_id') == 13275510:
                target_order = order
                break
        
        if target_order:
            logger.info("\n🎯 Target order #13275510 analysis:")
            raw_data = target_order.get('raw_data', {})
            products = raw_data.get('products', [])
            
            logger.info(f"   Klant: {target_order.get('klant_naam')}")
            logger.info(f"   Bestel datum: {target_order.get('bestel_datum')}")
            logger.info(f"   Origin song ID: {target_order.get('origin_song_id')}")
            
            logger.info("   Products:")
            for product in products:
                product_id = product.get('id')
                product_name = product.get('name', product.get('title', 'Unknown'))
                pivot_type = product.get('pivot', {}).get('type')
                logger.info(f"     ID: {product_id}, Name: {product_name}, Pivot type: {pivot_type}")
            
            # Check customer info
            customer = raw_data.get('customer', {})
            address = raw_data.get('address', {})
            logger.info(f"   Customer email: {customer.get('email', 'None')}")
            logger.info(f"   Address full_name: {address.get('full_name', 'None')}")
            logger.info(f"   Address firstname: {address.get('firstname', 'None')}")
            logger.info(f"   Address lastname: {address.get('lastname', 'None')}")
        
    except Exception as e:
        logger.error(f"❌ Error during investigation: {str(e)}")

if __name__ == "__main__":
    investigate_upsell_orders() 