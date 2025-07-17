#!/usr/bin/env python3
"""
Script om UpSell linking uit te voeren via de API.
"""

import requests
import logging

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_upsell_linking():
    """Voer UpSell linking uit via de API."""
    
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("🔗 Starting UpSell linking process...")
        
        # Voer UpSell linking uit
        response = requests.post(f"{BASE_URL}/orders/link-upsell-orders", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ UpSell linking successful!")
            logger.info(f"   Message: {result.get('message')}")
            logger.info(f"   Updated orders: {result.get('updated_count', 0)}")
            logger.info(f"   Total processed: {result.get('total_processed', 0)}")
            return True
        else:
            logger.error(f"❌ UpSell linking failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during UpSell linking: {str(e)}")
        return False

if __name__ == "__main__":
    run_upsell_linking() 