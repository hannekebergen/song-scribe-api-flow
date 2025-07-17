#!/usr/bin/env python3
"""
Test script voor songtekst synchronisatie tussen originele orders en UpSell orders.
"""

import os
import sys
import logging
import requests
from datetime import datetime

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_songtext_synchronization():
    """Test de songtekst synchronisatie functionaliteit."""
    
    BASE_URL = "http://localhost:8000"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("🎵 Testing Songtekst Synchronisatie")
        logger.info("=" * 50)
        
        # Stap 1: Haal alle orders op om een originele order en UpSell order te vinden
        logger.info("📋 Stap 1: Ophalen van orders...")
        response = requests.get(f"{BASE_URL}/orders/orders", headers=headers)
        
        if response.status_code != 200:
            logger.error(f"❌ Kon orders niet ophalen: {response.status_code}")
            return False
        
        orders = response.json()
        logger.info(f"✅ {len(orders)} orders opgehaald")
        
        # Stap 2: Zoek een originele order met songtekst
        original_order = None
        for order in orders:
            if order.get('songtekst') and order.get('songtekst').strip():
                # Check of dit geen UpSell order is
                if not order.get('origin_song_id'):
                    original_order = order
                    break
        
        if not original_order:
            logger.warning("⚠️ Geen originele order met songtekst gevonden")
            logger.info("💡 Maak eerst een songtekst aan in een originele order")
            return False
        
        logger.info(f"✅ Originele order gevonden: #{original_order['order_id']}")
        logger.info(f"   Songtekst: {original_order['songtekst'][:100]}...")
        
        # Stap 3: Zoek UpSell orders die gelinkt zijn aan deze originele order
        upsell_orders = []
        for order in orders:
            if order.get('origin_song_id') == original_order['order_id']:
                upsell_orders.append(order)
        
        if not upsell_orders:
            logger.warning("⚠️ Geen UpSell orders gevonden voor deze originele order")
            logger.info("💡 Voer eerst het UpSell linking proces uit")
            return False
        
        logger.info(f"✅ {len(upsell_orders)} UpSell orders gevonden")
        
        # Stap 4: Test songtekst synchronisatie
        logger.info("🔄 Stap 2: Testen van songtekst synchronisatie...")
        
        # Nieuwe songtekst voor de originele order
        new_songtext = f"""🎵 Nieuwe songtekst voor {original_order.get('klant_naam', 'onbekend')}

Dit is een test songtekst die automatisch gesynchroniseerd moet worden
naar alle gerelateerde UpSell orders.

Gegenereerd op: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Refrein:
🎶 La la la, dit is een test
🎶 Om te zien of synchronisatie werkt
🎶 Tussen originele en UpSell orders
🎶 Zodat alles up-to-date blijft!"""

        # Update de originele order
        update_response = requests.put(
            f"{BASE_URL}/orders/{original_order['order_id']}/songtext",
            headers=headers,
            json={
                "songtekst": new_songtext,
                "sync_to_upsells": True
            }
        )
        
        if update_response.status_code != 200:
            logger.error(f"❌ Kon songtekst niet updaten: {update_response.status_code}")
            logger.error(f"Response: {update_response.text}")
            return False
        
        logger.info("✅ Songtekst succesvol geüpdatet in originele order")
        
        # Stap 5: Controleer of UpSell orders zijn gesynchroniseerd
        logger.info("🔍 Stap 3: Controleren van synchronisatie...")
        
        # Haal orders opnieuw op om de wijzigingen te zien
        response = requests.get(f"{BASE_URL}/orders/orders", headers=headers)
        if response.status_code != 200:
            logger.error("❌ Kon orders niet opnieuw ophalen")
            return False
        
        updated_orders = response.json()
        
        # Zoek de bijgewerkte UpSell orders
        synced_count = 0
        for order in updated_orders:
            if order.get('origin_song_id') == original_order['order_id']:
                if order.get('songtekst') == new_songtext:
                    synced_count += 1
                    logger.info(f"✅ UpSell order #{order['order_id']} gesynchroniseerd")
                else:
                    logger.info(f"⚠️ UpSell order #{order['order_id']} niet gesynchroniseerd")
                    logger.info(f"   Huidige songtekst: {order.get('songtekst', 'Geen')[:50]}...")
        
        logger.info(f"📊 Synchronisatie resultaat: {synced_count}/{len(upsell_orders)} UpSell orders gesynchroniseerd")
        
        if synced_count > 0:
            logger.info("🎉 SUCCESS: Songtekst synchronisatie werkt!")
            return True
        else:
            logger.warning("⚠️ Geen UpSell orders gesynchroniseerd")
            return False
            
    except Exception as e:
        logger.error(f"❌ Fout tijdens test: {str(e)}")
        return False

def test_upsell_linking():
    """Test het UpSell linking proces."""
    
    BASE_URL = "http://localhost:8000"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("🔗 Testing UpSell Linking")
        logger.info("=" * 30)
        
        # Voer UpSell linking uit
        response = requests.post(f"{BASE_URL}/orders/link-upsell-orders", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ UpSell linking succesvol!")
            logger.info(f"   Message: {result.get('message')}")
            logger.info(f"   Updated orders: {result.get('updated_count', 0)}")
            return True
        else:
            logger.error(f"❌ UpSell linking gefaald: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Fout bij UpSell linking: {str(e)}")
        return False

def main():
    """Main test functie."""
    
    logger.info("🚀 Starting Songtekst Synchronisatie Test")
    logger.info(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    # Test UpSell linking eerst
    linking_success = test_upsell_linking()
    
    if linking_success:
        # Test songtekst synchronisatie
        sync_success = test_songtext_synchronization()
        
        if sync_success:
            logger.info("\n🎉 ALLE TESTS GESLAAGD!")
            logger.info("✅ UpSell linking werkt")
            logger.info("✅ Songtekst synchronisatie werkt")
            logger.info("\n💡 Je kunt nu:")
            logger.info("   1. Een songtekst opslaan in een originele order")
            logger.info("   2. De songtekst wordt automatisch zichtbaar in UpSell orders")
            logger.info("   3. UpSell orders tonen de originele songtekst")
        else:
            logger.error("\n❌ Songtekst synchronisatie test gefaald")
    else:
        logger.error("\n❌ UpSell linking test gefaald")
    
    logger.info("\n✨ Test voltooid!")

if __name__ == "__main__":
    main() 