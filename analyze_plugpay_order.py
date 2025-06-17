"""
Script to directly fetch and analyze an order from Plug&Pay API
This bypasses the database and focuses on the raw API data
"""

import os
import sys
import logging
import json
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("plugpay_analysis")

# Load environment variables from .env file if it exists
load_dotenv()

# Import the necessary functions from the app
from app.services.plugpay_client import get_order_details, get_custom_fields

def analyze_order(order_id):
    """
    Fetch and analyze an order directly from the Plug&Pay API
    """
    logger.info(f"Analyzing order #{order_id} from Plug&Pay API")
    
    try:
        # Fetch the order details from Plug&Pay
        order_details = get_order_details(order_id)
        logger.info(f"Successfully fetched order #{order_id}")
        
        # Log the structure of the order data
        logger.info(f"Order data structure:")
        logger.info(f"- Has custom_field_inputs: {'custom_field_inputs' in order_details}")
        if 'custom_field_inputs' in order_details:
            logger.info(f"  - Number of root-level custom_field_inputs: {len(order_details['custom_field_inputs'])}")
        
        logger.info(f"- Has custom_fields: {'custom_fields' in order_details}")
        if 'custom_fields' in order_details:
            logger.info(f"  - Number of root-level custom_fields: {len(order_details['custom_fields'])}")
        
        logger.info(f"- Has products: {'products' in order_details}")
        if 'products' in order_details:
            logger.info(f"  - Number of products: {len(order_details['products'])}")
            
            # Check each product for custom fields
            for i, product in enumerate(order_details['products']):
                logger.info(f"  - Product {i+1}:")
                logger.info(f"    - Has custom_field_inputs: {'custom_field_inputs' in product}")
                if 'custom_field_inputs' in product:
                    logger.info(f"      - Number of custom_field_inputs: {len(product['custom_field_inputs'])}")
                    
                    # Check for description fields in product custom_field_inputs
                    for field in product['custom_field_inputs']:
                        if field['label'] in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                            content_length = len(field['input']) if field['input'] else 0
                            logger.info(f"      - Found description field '{field['label']}' with {content_length} characters")
                            if content_length > 0:
                                logger.info(f"      - Preview: {field['input'][:100]}...")
                
                logger.info(f"    - Has custom_fields: {'custom_fields' in product}")
                if 'custom_fields' in product:
                    logger.info(f"      - Number of custom_fields: {len(product['custom_fields'])}")
                    
                    # Check for description fields in product custom_fields
                    for field_name, field_value in product['custom_fields'].items():
                        if field_name in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                            content_length = len(field_value) if field_value else 0
                            logger.info(f"      - Found description field '{field_name}' with {content_length} characters")
                            if content_length > 0:
                                logger.info(f"      - Preview: {field_value[:100]}...")
        
        logger.info(f"- Has address: {'address' in order_details}")
        if 'address' in order_details and order_details['address']:
            logger.info(f"  - Has note: {'note' in order_details['address']}")
            if 'note' in order_details['address'] and order_details['address']['note']:
                note = order_details['address']['note']
                logger.info(f"  - Note length: {len(note)}")
                logger.info(f"  - Preview: {note[:100]}...")
        
        # Extract custom fields using the same function as in the app
        logger.info("\nExtracting custom fields using get_custom_fields function:")
        custom_fields = get_custom_fields(order_details)
        logger.info(f"Found {len(custom_fields)} custom fields:")
        for field_name, field_value in custom_fields.items():
            if field_name in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                content_length = len(field_value) if field_value else 0
                logger.info(f"- {field_name}: {content_length} characters")
                if content_length > 0:
                    logger.info(f"  Preview: {field_value[:100]}...")
            else:
                logger.info(f"- {field_name}: {field_value}")
        
        # Check for description fields
        description_fields = [field for field in custom_fields.keys() 
                             if field in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid",
                                         "Vertel iets over deze persoon", "Toelichting", "Vertel over de persoon",
                                         "Vertel over deze persoon", "Vertel over je wensen", "Vertel over je ideeën",
                                         "Vertel je verhaal", "Vertel meer", "Vertel"]]
        
        if description_fields:
            logger.info(f"\nFound {len(description_fields)} description fields: {', '.join(description_fields)}")
            for field in description_fields:
                content_length = len(custom_fields[field]) if custom_fields[field] else 0
                logger.info(f"- {field}: {content_length} characters")
        else:
            logger.info("\nNo description fields found in custom fields")
            
            # Check for alternative fields that might contain descriptions
            alt_fields = []
            for field_name in custom_fields.keys():
                if any(keyword in field_name.lower() for keyword in ["opmerking", "notitie", "wens", "idee", "verhaal", "vertel", "beschrijf"]):
                    alt_fields.append(field_name)
            
            if alt_fields:
                logger.info(f"Found {len(alt_fields)} alternative fields that might contain descriptions: {', '.join(alt_fields)}")
            else:
                logger.info("No alternative fields found that might contain descriptions")
        
        # Save the raw order data to a file for further analysis
        output_file = f"order_{order_id}_raw_data.json"
        with open(output_file, 'w') as f:
            json.dump(order_details, f, indent=2)
        logger.info(f"\nSaved raw order data to {output_file}")
        
        return order_details
        
    except Exception as e:
        logger.error(f"Error analyzing order: {str(e)}")
        return None

if __name__ == "__main__":
    # Check if order ID is provided as command line argument
    if len(sys.argv) > 1:
        order_id = sys.argv[1]
    else:
        # Default to the order ID we're investigating
        order_id = "12946543"
    
    analyze_order(order_id)
