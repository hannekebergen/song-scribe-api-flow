#!/usr/bin/env python3
"""
Script om een Upsell order handmatig te linken aan een originele order via de API.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def link_upsell_to_original(upsell_order_id, original_order_id):
    BASE_URL = "https://jouwsong-api.onrender.com"
    API_KEY = "jouwsong2025"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"original_order_id": original_order_id}
    
    try:
        logger.info(f"🔗 Linking Upsell order #{upsell_order_id} to original order #{original_order_id}...")
        response = requests.post(
            f"{BASE_URL}/orders/upsell-matches/{upsell_order_id}/link",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            logger.info("✅ Upsell order succesvol gelinkt!")
            logger.info(f"Response: {response.json()}")
        else:
            logger.error(f"❌ Fout bij linken: {response.status_code}")
            logger.error(f"Response: {response.text}")
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    link_upsell_to_original(13275510, 13275506) 