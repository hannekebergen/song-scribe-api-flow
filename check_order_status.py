#!/usr/bin/env python3
"""
Script om de status van een specifieke order te controleren.
"""

import requests
import logging

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_order_status(order_id):
    """Controleer de status van een specifieke order."""
    
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"🔍 Checking status of order #{order_id}...")
        
        # Haal order details op
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
        
        if response.status_code == 200:
            order = response.json()
            logger.info("✅ Order details retrieved!")
            
            # Toon belangrijke velden
            logger.info(f"   Order ID: {order.get('order_id')}")
            logger.info(f"   Klant Naam: {order.get('klant_naam')}")
            logger.info(f"   Voornaam: {order.get('voornaam')}")
            logger.info(f"   Bestel Datum: {order.get('bestel_datum')}")
            logger.info(f"   Thema: {order.get('thema')}")
            logger.info(f"   Origin Song ID: {order.get('origin_song_id')}")
            logger.info(f"   Songtekst: {order.get('songtekst', 'Niet ingesteld')[:100]}...")
            
            # Check of dit een Upsell order is
            raw_data = order.get('raw_data', {})
            products = raw_data.get('products', [])
            
            is_upsell = False
            for product in products:
                pivot_type = product.get('pivot', {}).get('type')
                if pivot_type == "upsell":
                    is_upsell = True
                    logger.info(f"   Product: {product.get('name')} (Upsell)")
                    break
            
            if not is_upsell:
                logger.info("   Type: Normale order")
            
            # Als het een Upsell order is, check de originele order
            if is_upsell and order.get('origin_song_id'):
                logger.info(f"\n🔗 Upsell order is gelinkt aan originele order #{order.get('origin_song_id')}")
                
                # Haal originele order op
                orig_response = requests.get(f"{BASE_URL}/orders/{order.get('origin_song_id')}", headers=headers)
                if orig_response.status_code == 200:
                    orig_order = orig_response.json()
                    logger.info(f"   Originele order thema: {orig_order.get('thema')}")
                    logger.info(f"   Originele order songtekst: {orig_order.get('songtekst', 'Niet ingesteld')[:100]}...")
                else:
                    logger.warning(f"   Kan originele order niet ophalen: {orig_response.status_code}")
            
            elif is_upsell:
                logger.warning("⚠️ Upsell order is NIET gelinkt aan een originele order!")
                
                # Zoek mogelijke matches
                logger.info("\n🔍 Zoeken naar mogelijke originele orders...")
                matches_response = requests.get(f"{BASE_URL}/orders/upsell-matches/{order_id}", headers=headers)
                
                if matches_response.status_code == 200:
                    matches_data = matches_response.json()
                    matches = matches_data.get('matches', [])
                    
                    if matches:
                        logger.info(f"   Gevonden {len(matches)} mogelijke matches:")
                        for match in matches[:3]:  # Toon eerste 3
                            logger.info(f"     Order #{match['order_id']}: {match['klant_naam']} (confidence: {match['confidence']}%)")
                    else:
                        logger.info("   Geen mogelijke matches gevonden")
                else:
                    logger.warning(f"   Kan matches niet ophalen: {matches_response.status_code}")
            
            return order
            
        else:
            logger.error(f"❌ Could not fetch order: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error checking order status: {str(e)}")
        return None

if __name__ == "__main__":
    # Check de Upsell order #13275510
    check_order_status(13275510) 