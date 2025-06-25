#!/usr/bin/env python3
"""
Test script voor UpSell order linking functionaliteit.
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

def main():
    """Test de UpSell linking functionaliteit."""
    
    BASE_URL = "http://localhost:8000"
    API_KEY = os.getenv("PLUGPAY_API_KEY", "your_api_key_here")
    
    if API_KEY == "your_api_key_here":
        logger.error("Stel eerst de PLUGPAY_API_KEY environment variable in")
        return False
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    try:
        logger.info("🔗 Testing UpSell linking functionaliteit...")
        
        # Test de link-upsell-orders endpoint
        logger.info("\n🔗 UpSell linking uitvoeren...")
        response = requests.post(f"{BASE_URL}/api/orders/link-upsell-orders", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ UpSell linking succesvol!")
            logger.info(f"   - Message: {result.get('message')}")
            logger.info(f"   - Updated orders: {result.get('updated_orders', 0)}")
        else:
            logger.error(f"❌ Fout bij UpSell linking: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
        
        logger.info(f"\n🎉 Test voltooid!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Fout: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 