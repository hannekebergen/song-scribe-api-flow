#!/usr/bin/env python3
"""
Production Order Refresh Script

Dit script refresht alle orders in de production database met de nieuwe
gecombineerde v1+v2 API data-ophaling voor maximale klantnaam extractie.
"""

import requests
import json
import time
import logging

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production API configuratie
BASE_URL = "https://jouwsong-api.onrender.com"
API_KEY = "jouwsong2025"

def refresh_production_orders():
    """Refresh alle orders in productie met nieuwe data."""
    logger.info("🔄 Refreshing production orders met verbeterde data-ophaling...")
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Stap 1: Fetch fresh orders from Plug&Pay
        logger.info("📡 Step 1: Fetching fresh orders from Plug&Pay...")
        fetch_url = f"{BASE_URL}/orders/fetch"
        fetch_response = requests.post(fetch_url, headers=headers, timeout=120)
        
        if fetch_response.status_code == 200:
            fetch_result = fetch_response.json()
            logger.info(f"✅ Fetch result: {fetch_result}")
        else:
            logger.warning(f"⚠️ Fetch failed: {fetch_response.status_code} - {fetch_response.text}")
        
        # Wacht even voor de database updates
        time.sleep(5)
        
        # Stap 2: Update names met nieuwe data
        logger.info("👤 Step 2: Updating names with improved extraction...")
        update_url = f"{BASE_URL}/orders/update-names"
        update_response = requests.post(update_url, headers=headers, timeout=120)
        
        if update_response.status_code == 200:
            update_result = update_response.json()
            logger.info(f"✅ Update result: {update_result}")
            
            updated_count = update_result.get('updated_count', 0)
            total_processed = update_result.get('total_processed', 0)
            success_rate = (updated_count / total_processed * 100) if total_processed > 0 else 0
            
            logger.info(f"📊 Final Results:")
            logger.info(f"   🎯 Success rate: {success_rate:.1f}% ({updated_count}/{total_processed})")
            logger.info(f"   ✅ Orders with names: {updated_count}")
            logger.info(f"   📦 Total orders: {total_processed}")
            
            if success_rate > 50:
                logger.info(f"🎉 Excellent! Success rate above 50%")
            elif success_rate > 25:
                logger.info(f"✅ Good improvement! Success rate above 25%")
            else:
                logger.info(f"📈 Some improvement, but room for more")
                
        else:
            logger.error(f"❌ Update failed: {update_response.status_code} - {update_response.text}")
        
        # Stap 3: Test een paar orders
        logger.info("🧪 Step 3: Testing a few orders...")
        test_orders(headers)
        
    except Exception as e:
        logger.error(f"❌ Error during production refresh: {e}")

def test_orders(headers):
    """Test een paar orders om de verbetering te zien."""
    try:
        # Haal orders op
        orders_url = f"{BASE_URL}/orders"
        response = requests.get(orders_url, headers=headers, params={"limit": 5})
        
        if response.status_code == 200:
            orders = response.json()
            logger.info(f"🧪 Testing {len(orders)} sample orders:")
            
            for i, order in enumerate(orders[:5], 1):
                klantnaam = order.get('klant_naam', 'Onbekend')
                order_id = order.get('order_id', 'N/A')
                logger.info(f"   {i}. Order {order_id}: '{klantnaam}'")
                
        else:
            logger.warning(f"⚠️ Could not fetch orders for testing: {response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ Error testing orders: {e}")

def check_api_status():
    """Check of de API online is."""
    try:
        # Test met orders endpoint
        orders_url = f"{BASE_URL}/orders"
        headers = {"X-API-Key": API_KEY}
        response = requests.get(orders_url, headers=headers, params={"limit": 1}, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"✅ API is online and healthy")
            return True
        else:
            logger.error(f"❌ API health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ API not reachable: {e}")
        return False

def main():
    """Hoofdfunctie."""
    logger.info("🚀 Production Order Refresh - Verbeterde Klantnaam Extractie")
    logger.info("=" * 70)
    
    # Check API status
    if not check_api_status():
        logger.error("❌ API is not available. Aborting.")
        return
    
    # Refresh orders
    refresh_production_orders()
    
    logger.info("\n🎯 Refresh complete!")
    logger.info("💡 Check het dashboard om de verbeterde klantnamen te zien:")
    logger.info("   https://song-scribe-api-flow.vercel.app/")

if __name__ == "__main__":
    main() 