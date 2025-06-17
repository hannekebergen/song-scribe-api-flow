"""
Script to directly test the order description extraction without database dependencies
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

logger = logging.getLogger("order_direct_test")

# Load environment variables from .env.temp file
load_dotenv(".env.temp")

# Get API key from environment
PLUGPAY_API_KEY = os.getenv("PLUGPAY_API_KEY")
if not PLUGPAY_API_KEY:
    logger.error("PLUGPAY_API_KEY not found in environment variables")
    sys.exit(1)

# API headers
api_headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {PLUGPAY_API_KEY}"
}

def get_order_details(order_id):
    """
    Fetch order details directly from Plug&Pay API
    This is a simplified version of the function in plugpay_client.py
    """
    logger.info(f"Fetching order #{order_id} from Plug&Pay API")
    
    # First API call to get order details
    url = f"https://api.plugpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products.custom_field_inputs,address"
    
    try:
        response = requests.get(url, headers=api_headers)
        response.raise_for_status()
        order_details = response.json()
        
        # Check if we have custom_field_inputs
        if 'custom_field_inputs' not in order_details or not order_details['custom_field_inputs']:
            logger.warning(f"No custom_field_inputs found in order {order_id}, retrying with explicit include")
            
            # Retry with explicit include parameters
            retry_url = f"https://api.plugpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products.custom_field_inputs,custom_fields,products.custom_fields,address"
            retry_response = requests.get(retry_url, headers=api_headers)
            retry_response.raise_for_status()
            order_details = retry_response.json()
        
        # Merge product-level custom fields into root-level
        if 'products' in order_details and order_details['products']:
            for product in order_details['products']:
                if 'custom_field_inputs' in product and product['custom_field_inputs']:
                    logger.info(f"Merging {len(product['custom_field_inputs'])} product-level custom_field_inputs")
                    
                    # Initialize custom_field_inputs at root level if not present
                    if 'custom_field_inputs' not in order_details:
                        order_details['custom_field_inputs'] = []
                    
                    # Add product-level custom fields to root level
                    for field in product['custom_field_inputs']:
                        order_details['custom_field_inputs'].append(field)
        
        return order_details
        
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        return None

def get_custom_fields(order_data):
    """
    Extract custom fields from order data
    This is a simplified version of the function in plugpay_client.py
    """
    custom_fields = {}
    order_id = order_data.get("id", "unknown")
    
    # Step 1: Extract from root-level custom_field_inputs (new format)
    if "custom_field_inputs" in order_data and order_data["custom_field_inputs"]:
        logger.info(f"Found {len(order_data['custom_field_inputs'])} root-level custom_field_inputs")
        for field in order_data["custom_field_inputs"]:
            if "label" in field and "input" in field:
                custom_fields[field["label"]] = field["input"]
                logger.info(f"Extracted field '{field['label']}' from root-level custom_field_inputs")
    
    # Step 2: Extract from root-level custom_fields (old format)
    if "custom_fields" in order_data and order_data["custom_fields"]:
        logger.info(f"Found root-level custom_fields (old format)")
        for field_name, field_value in order_data["custom_fields"].items():
            custom_fields[field_name] = field_value
            logger.info(f"Extracted field '{field_name}' from root-level custom_fields")
    
    # Step 3: Extract from product-level custom fields
    if "products" in order_data and order_data["products"]:
        for product_idx, product in enumerate(order_data["products"]):
            # Try new format (custom_field_inputs)
            if "custom_field_inputs" in product and product["custom_field_inputs"]:
                logger.info(f"Product {product_idx} has {len(product['custom_field_inputs'])} custom_field_inputs")
                for field in product["custom_field_inputs"]:
                    if "label" in field and "input" in field:
                        custom_fields[field["label"]] = field["input"]
                        logger.info(f"Extracted field '{field['label']}' from product-level custom_field_inputs")
            
            # Try old format (custom_fields)
            if "custom_fields" in product and product["custom_fields"]:
                logger.info(f"Product {product_idx} has custom_fields (old format)")
                for field_name, field_value in product["custom_fields"].items():
                    custom_fields[field_name] = field_value
                    logger.info(f"Extracted field '{field_name}' from product-level custom_fields")
    
    # Step 4: Add personal story from address.note if it exists
    if "address" in order_data and order_data["address"] and "note" in order_data["address"]:
        note = order_data["address"]["note"]
        if note and len(note.strip()) > 0:
            custom_fields["Beschrijf"] = note
            logger.info(f"Added personal story from address.note with length {len(note)}")
    
    return custom_fields

def map_custom_fields_to_order(custom_fields, order_id):
    """
    Map custom fields to order attributes
    This simulates the field mapping in orders.py
    """
    # Create a simple order object to hold the mapped fields
    order = {"order_id": order_id}
    
    # Define the field mapping (same as in orders.py)
    field_mapping = {
        # Voornaam varianten
        "Voornaam": "voornaam",
        "Voor wie is het lied?": "voornaam",
        "Voor wie": "voornaam",
        
        # Achternaam varianten
        "Achternaam": "van_naam",
        "Van": "van_naam",
        
        # Relatie varianten
        "Relatie": "relatie",
        "Wat is je relatie tot deze persoon?": "relatie",
        
        # Datum varianten
        "Datum": "datum",
        "Wanneer": "datum",
        "Wanneer is het lied nodig?": "datum",
        "Deadline": "datum",
        
        # Thema varianten
        "Thema": "thema",
        "Gelegenheid": "thema",
        
        # Toon varianten
        "Toon": "toon",
        "Gewenste toon": "toon",
        "Stijl": "toon",
        
        # Structuur varianten
        "Structuur": "structuur",
        "Opbouw": "structuur",
        
        # Rijm varianten
        "Rijm": "rijm",
        "Rijmschema": "rijm",
        
        # Beschrijving varianten
        "Beschrijf": "beschrijving",
        "Persoonlijk verhaal": "beschrijving",
        "Vertel iets over deze persoon": "beschrijving",
        "Toelichting": "beschrijving",
        "Vertel over de gelegenheid": "beschrijving",
        "Vertel over de persoon": "beschrijving",
        "Vertel over deze persoon": "beschrijving",
        "Vertel over je wensen": "beschrijving",
        "Vertel over je ideeën": "beschrijving",
        "Vertel je verhaal": "beschrijving",
        "Vertel meer": "beschrijving",
        "Vertel": "beschrijving",
    }
    
    # Map custom fields to order attributes
    mapped_fields = 0
    for field_name, field_value in custom_fields.items():
        # Check if this field is in our mapping
        if field_name in field_mapping:
            attr_name = field_mapping[field_name]
            order[attr_name] = field_value
            mapped_fields += 1
            logger.info(f"Custom field '{field_name}' mapped to '{attr_name}'")
    
    # Log result
    logger.info(f"{mapped_fields} custom fields mapped to order attributes")
    
    # Final verification for critical fields
    if "beschrijving" in order and order["beschrijving"]:
        desc_length = len(order["beschrijving"])
        logger.info(f"Final beschrijving field has {desc_length} characters")
        logger.info(f"Content preview: {order['beschrijving'][:100]}..." if desc_length > 100 else order['beschrijving'])
    else:
        logger.warning(f"No beschrijving field was mapped or it's empty")
    
    return order

def analyze_order(order_id):
    """
    Analyze an order by fetching it from the API and processing its fields
    """
    logger.info(f"=== Analyzing order #{order_id} ===")
    
    # Fetch order details
    order_details = get_order_details(order_id)
    if not order_details:
        logger.error(f"Failed to fetch order #{order_id}")
        return
    
    # Extract custom fields
    custom_fields = get_custom_fields(order_details)
    
    # Map custom fields to order
    order = map_custom_fields_to_order(custom_fields, order_id)
    
    # Print the final order object
    logger.info(f"=== Final order object for #{order_id} ===")
    for key, value in order.items():
        if key == "beschrijving" and value:
            logger.info(f"{key}: {value[:50]}... ({len(value)} chars)")
        else:
            logger.info(f"{key}: {value}")
    
    # Save the raw order data to a file for further analysis
    output_file = f"order_{order_id}_raw_data.json"
    with open(output_file, 'w') as f:
        json.dump(order_details, f, indent=2)
    logger.info(f"Saved raw order data to {output_file}")
    
    # Save the extracted custom fields to a file
    fields_file = f"order_{order_id}_custom_fields.json"
    with open(fields_file, 'w') as f:
        json.dump(custom_fields, f, indent=2)
    logger.info(f"Saved custom fields to {fields_file}")
    
    return order_details, custom_fields, order

if __name__ == "__main__":
    # Check if order ID is provided as command line argument
    if len(sys.argv) > 1:
        order_id = sys.argv[1]
    else:
        # Default to the order ID we're investigating
        order_id = "12946543"
    
    analyze_order(order_id)
