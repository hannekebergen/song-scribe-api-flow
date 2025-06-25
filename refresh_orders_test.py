#!/usr/bin/env python3
"""Test script voor verbeterde order data ophaling"""

import os
import sys
import logging
from dotenv import load_dotenv

# Setup
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.services.plugpay_client import get_order_details

def test_improved_fetching():
    """Test de nieuwe gecombineerde data ophaling."""
    logger.info("🧪 Testing improved order data fetching...")
    
    try:
        # Test met een bekende order ID
        order_id = "13052893"  # Van eerdere test
        
        logger.info(f"🎯 Testing with order {order_id}")
        order_details = get_order_details(order_id)
        
        # Analyseer resultaten
        has_address = bool(order_details.get('address'))
        has_custom_fields = bool(order_details.get('custom_field_inputs'))
        has_items = bool(order_details.get('items'))
        
        logger.info(f"📊 Results:")
        logger.info(f"   Address: {has_address}")
        logger.info(f"   Custom fields: {has_custom_fields} ({len(order_details.get('custom_field_inputs', []))} fields)")
        logger.info(f"   Items: {has_items} ({len(order_details.get('items', []))} items)")
        
        if has_address:
            addr = order_details['address']
            logger.info(f"   👤 Name: {addr.get('full_name', 'N/A')}")
            
        if has_custom_fields:
            for field in order_details['custom_field_inputs'][:3]:
                logger.info(f"   📝 {field.get('name')}: {field.get('value')}")
                
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_improved_fetching() 