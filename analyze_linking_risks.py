#!/usr/bin/env python3
"""
Script om de risico's van UpSell linking te analyseren.
"""

import requests
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_linking_risks():
    """Analyseer de risico's van de huidige UpSell linking logica."""
    
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("🔍 Analyzing UpSell linking risks...")
        
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
        
        logger.info(f"📊 Found {len(original_orders)} original orders and {len(upsell_orders)} upsell orders")
        
        # Risico 1: Klanten met dezelfde voornaam
        logger.info("\n🚨 RISK 1: Customers with same first name")
        firstname_counts = defaultdict(list)
        
        for order in original_orders:
            voornaam = order.get('voornaam')
            if voornaam:
                firstname_counts[voornaam].append(order)
        
        risky_firstnames = {name: orders for name, orders in firstname_counts.items() if len(orders) > 1}
        
        if risky_firstnames:
            logger.warning(f"⚠️ Found {len(risky_firstnames)} first names with multiple orders:")
            for name, orders in list(risky_firstnames.items())[:5]:  # Toon eerste 5
                logger.warning(f"   '{name}': {len(orders)} orders")
                for order in orders[:3]:  # Toon eerste 3 orders
                    logger.warning(f"     Order #{order['order_id']}: {order.get('klant_naam')} - {order.get('bestel_datum')}")
        else:
            logger.info("✅ No risky first names found")
        
        # Risico 2: Klanten met meerdere orders in korte tijd
        logger.info("\n🚨 RISK 2: Customers with multiple orders in short time")
        customer_orders = defaultdict(list)
        
        for order in original_orders:
            klant_naam = order.get('klant_naam')
            if klant_naam:
                customer_orders[klant_naam].append(order)
        
        risky_customers = {}
        for customer, orders in customer_orders.items():
            if len(orders) > 1:
                # Sorteer op datum
                sorted_orders = sorted(orders, key=lambda x: x.get('bestel_datum', ''))
                
                # Check voor orders binnen 7 dagen
                for i, order1 in enumerate(sorted_orders):
                    for order2 in sorted_orders[i+1:]:
                        try:
                            date1 = datetime.fromisoformat(order1.get('bestel_datum', '').replace('Z', '+00:00'))
                            date2 = datetime.fromisoformat(order2.get('bestel_datum', '').replace('Z', '+00:00'))
                            days_diff = (date2 - date1).days
                            
                            if days_diff <= 7:
                                if customer not in risky_customers:
                                    risky_customers[customer] = []
                                risky_customers[customer].append((order1, order2, days_diff))
                        except:
                            pass
        
        if risky_customers:
            logger.warning(f"⚠️ Found {len(risky_customers)} customers with multiple orders within 7 days:")
            for customer, order_pairs in list(risky_customers.items())[:3]:  # Toon eerste 3
                logger.warning(f"   '{customer}': {len(order_pairs)} order pairs")
                for order1, order2, days_diff in order_pairs[:2]:  # Toon eerste 2 pairs
                    logger.warning(f"     Order #{order1['order_id']} and #{order2['order_id']} ({days_diff} days apart)")
        else:
            logger.info("✅ No risky customer order patterns found")
        
        # Risico 3: UpSell orders zonder duidelijke match
        logger.info("\n🚨 RISK 3: UpSell orders without clear match")
        unmatched_upsells = []
        
        for upsell in upsell_orders:
            upsell_id = upsell.get('order_id')
            klant_naam = upsell.get('klant_naam')
            voornaam = upsell.get('voornaam')
            bestel_datum = upsell.get('bestel_datum')
            origin_song_id = upsell.get('origin_song_id')
            
            if not origin_song_id:  # Nog niet gelinkt
                # Zoek potentiële matches
                potential_matches = []
                
                for original in original_orders:
                    if original.get('klant_naam') == klant_naam:
                        try:
                            upsell_date = datetime.fromisoformat(bestel_datum.replace('Z', '+00:00'))
                            original_date = datetime.fromisoformat(original.get('bestel_datum', '').replace('Z', '+00:00'))
                            days_diff = (upsell_date - original_date).days
                            
                            if 0 <= days_diff <= 7:  # Originele order voor UpSell, binnen 7 dagen
                                potential_matches.append((original, days_diff))
                        except:
                            pass
                
                if len(potential_matches) > 1:
                    unmatched_upsells.append((upsell, potential_matches))
        
        if unmatched_upsells:
            logger.warning(f"⚠️ Found {len(unmatched_upsells)} UpSell orders with multiple potential matches:")
            for upsell, matches in unmatched_upsells[:3]:  # Toon eerste 3
                logger.warning(f"   UpSell #{upsell['order_id']} ({upsell.get('klant_naam')}):")
                for original, days_diff in matches:
                    logger.warning(f"     Could match Order #{original['order_id']} ({days_diff} days before)")
        else:
            logger.info("✅ No UpSell orders with multiple potential matches")
        
        # Risico 4: Al gelinkte orders controleren
        logger.info("\n🚨 RISK 4: Checking already linked orders")
        linked_upsells = [o for o in upsell_orders if o.get('origin_song_id')]
        
        if linked_upsells:
            logger.info(f"📊 Found {len(linked_upsells)} already linked UpSell orders")
            
            # Check voor dubbele links
            origin_counts = defaultdict(list)
            for upsell in linked_upsells:
                origin_id = upsell.get('origin_song_id')
                origin_counts[origin_id].append(upsell)
            
            multiple_upsells = {origin_id: upsells for origin_id, upsells in origin_counts.items() if len(upsells) > 1}
            
            if multiple_upsells:
                logger.info(f"✅ Found {len(multiple_upsells)} original orders with multiple UpSell orders (this is normal)")
                for origin_id, upsells in list(multiple_upsells.items())[:3]:
                    logger.info(f"   Original #{origin_id}: {len(upsells)} UpSell orders")
            else:
                logger.info("✅ All original orders have single UpSell orders")
        
        # Aanbevelingen
        logger.info("\n💡 RECOMMENDATIONS:")
        logger.info("1. Add confidence scoring to linking algorithm")
        logger.info("2. Implement manual review for ambiguous matches")
        logger.info("3. Add validation checks for linked orders")
        logger.info("4. Consider using email as primary matching key")
        logger.info("5. Add logging for all linking decisions")
        
    except Exception as e:
        logger.error(f"❌ Error during risk analysis: {str(e)}")

if __name__ == "__main__":
    analyze_linking_risks() 