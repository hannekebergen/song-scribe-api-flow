#!/usr/bin/env python3
"""
Script om de originele order te vinden voor een specifieke klant.
"""

import requests
import logging
from datetime import datetime

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_original_order_for_customer(customer_name):
    """Zoek originele orders voor een specifieke klant."""
    
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"🔍 Zoeken naar orders voor klant: {customer_name}")
        
        # Haal alle orders op
        response = requests.get(f"{BASE_URL}/orders/orders", headers=headers)
        
        if response.status_code == 200:
            orders = response.json()
            logger.info(f"📋 Found {len(orders)} total orders")
            
            # Filter orders voor deze klant
            customer_orders = []
            
            for order in orders:
                order_klant_naam = order.get('klant_naam') or ''
                order_voornaam = order.get('voornaam') or ''
                
                # Check verschillende naam variaties
                if (customer_name.lower() in order_klant_naam.lower() or 
                    customer_name.lower() in order_voornaam.lower() or
                    order_klant_naam.lower() in customer_name.lower()):
                    
                    customer_orders.append(order)
            
            logger.info(f"👤 Found {len(customer_orders)} orders for {customer_name}")
            
            if customer_orders:
                # Sorteer op datum
                customer_orders.sort(key=lambda x: x.get('bestel_datum', ''))
                
                logger.info("\n📅 Orders voor deze klant:")
                for order in customer_orders:
                    order_id = order.get('order_id')
                    bestel_datum = order.get('bestel_datum')
                    thema = order.get('thema')
                    origin_song_id = order.get('origin_song_id')
                    
                    # Check of dit een Upsell order is
                    raw_data = order.get('raw_data', {})
                    products = raw_data.get('products', [])
                    
                    is_upsell = False
                    product_name = "Onbekend"
                    for product in products:
                        pivot_type = product.get('pivot', {}).get('type')
                        if pivot_type == "upsell":
                            is_upsell = True
                            product_name = product.get('name', 'Upsell')
                            break
                        else:
                            product_name = product.get('name', 'Normaal')
                    
                    order_type = "🔗 Upsell" if is_upsell else "📝 Origineel"
                    link_status = f" (gelinkt aan #{origin_song_id})" if origin_song_id else " (niet gelinkt)"
                    
                    logger.info(f"   {order_type} #{order_id}: {product_name}")
                    logger.info(f"      Datum: {bestel_datum}")
                    logger.info(f"      Thema: {thema}")
                    logger.info(f"      Status: {order_type}{link_status}")
                    logger.info("")
                
                # Zoek de originele order (eerste niet-Upsell order)
                original_orders = [o for o in customer_orders if not any(
                    p.get('pivot', {}).get('type') == "upsell" 
                    for p in o.get('raw_data', {}).get('products', [])
                )]
                
                if original_orders:
                    logger.info("🎯 Originele orders gevonden:")
                    for order in original_orders:
                        logger.info(f"   Order #{order.get('order_id')}: {order.get('thema')}")
                        
                        # Check of deze order songtekst heeft
                        songtekst = order.get('songtekst', '')
                        if songtekst and songtekst.strip():
                            logger.info(f"   ✅ Heeft songtekst: {songtekst[:100]}...")
                        else:
                            logger.info(f"   ❌ Geen songtekst")
                else:
                    logger.warning("⚠️ Geen originele orders gevonden voor deze klant")
                
                return customer_orders
            else:
                logger.warning(f"⚠️ Geen orders gevonden voor klant: {customer_name}")
                return []
                
        else:
            logger.error(f"❌ Could not fetch orders: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ Error finding original order: {str(e)}")
        return []

if __name__ == "__main__":
    # Zoek orders voor Nadia Carsinetti
    find_original_order_for_customer("Nadia Carsinetti") 