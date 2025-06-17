"""
Test script to diagnose issues with description field extraction from orders.
This script simulates the processing logic in orders.py without requiring database access.
"""

import logging
import sys
import json
from sample_order_data import (
    sample_order, 
    sample_order_with_note, 
    sample_order_no_description,
    sample_order_old_format,
    sample_order_alt_description
)

# Configure logging to output to console
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("description_extraction")

def extract_custom_fields(order_data):
    """
    Extract custom fields from order data, simulating the logic in orders.py
    """
    order_id = order_data.get("order_id", "unknown")
    custom_fields = {}
    
    # Step 1: Extract from root-level custom_field_inputs (new format)
    if "custom_field_inputs" in order_data and order_data["custom_field_inputs"]:
        logger.info(f"Order {order_id}: Found {len(order_data['custom_field_inputs'])} root-level custom_field_inputs")
        for field in order_data["custom_field_inputs"]:
            custom_fields[field["label"]] = field["input"]
            logger.info(f"Order {order_id}: Found field '{field['label']}' in root-level custom_field_inputs")
            
            # Log the content length for description fields
            if field["label"] in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                content_length = len(field["input"]) if field["input"] else 0
                logger.info(f"Order {order_id}: Field '{field['label']}' has content length of {content_length} characters")
    else:
        logger.info(f"Order {order_id}: No root-level custom_field_inputs found")
    
    # Step 2: Extract from root-level custom_fields (old format)
    if "custom_fields" in order_data and order_data["custom_fields"]:
        logger.info(f"Order {order_id}: Found root-level custom_fields (old format)")
        for field_name, field_value in order_data["custom_fields"].items():
            custom_fields[field_name] = field_value
            logger.info(f"Order {order_id}: Found field '{field_name}' in root-level custom_fields")
            
            # Log the content length for description fields
            if field_name in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                content_length = len(field_value) if field_value else 0
                logger.info(f"Order {order_id}: Field '{field_name}' has content length of {content_length} characters")
    else:
        logger.info(f"Order {order_id}: No root-level custom_fields found")
    
    # Step 3: Extract product-level custom fields
    product_fields_found = False
    if "products" in order_data and order_data["products"]:
        logger.info(f"Order {order_id}: Found {len(order_data['products'])} products")
        for product_idx, product in enumerate(order_data["products"]):
            logger.info(f"Order {order_id}: Checking product {product_idx}")
            
            # Try new format (custom_field_inputs)
            if "custom_field_inputs" in product and product["custom_field_inputs"]:
                logger.info(f"Order {order_id}: Product {product_idx} has {len(product['custom_field_inputs'])} custom_field_inputs")
                for field in product["custom_field_inputs"]:
                    custom_fields[field["label"]] = field["input"]
                    product_fields_found = True
                    logger.info(f"Order {order_id}: Found field '{field['label']}' in product-level custom_field_inputs")
                    
                    # Log the content length for description fields
                    if field["label"] in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                        content_length = len(field["input"]) if field["input"] else 0
                        logger.info(f"Order {order_id}: Field '{field['label']}' has content length of {content_length} characters")
                        logger.info(f"Order {order_id}: Content preview: {field['input'][:100]}..." if field["input"] else "Empty content")
            
            # Try old format (custom_fields)
            if "custom_fields" in product and product["custom_fields"]:
                logger.info(f"Order {order_id}: Product {product_idx} has custom_fields (old format)")
                for field_name, field_value in product["custom_fields"].items():
                    custom_fields[field_name] = field_value
                    product_fields_found = True
                    logger.info(f"Order {order_id}: Found field '{field_name}' in product-level custom_fields")
    else:
        logger.info(f"Order {order_id}: No products found")
    
    # Check if any product-level fields were found
    if product_fields_found:
        logger.info(f"Order {order_id}: Successfully found custom fields in products")
    else:
        logger.info(f"Order {order_id}: No custom fields found in products")
    
    # Step 4: Add personal story from address.note if it exists
    if "address" in order_data and order_data["address"] and "note" in order_data["address"]:
        note = order_data["address"]["note"]
        if note and len(note.strip()) > 0:
            custom_fields["Beschrijf"] = note
            logger.info(f"Order {order_id}: Found personal story in address.note with length {len(note)}")
            logger.info(f"Order {order_id}: Content preview: {note[:100]}..." if len(note) > 100 else note)
        else:
            logger.info(f"Order {order_id}: address.note is empty or only whitespace")
    else:
        logger.info(f"Order {order_id}: No address.note found")
    
    # Step 5: Check if we have a description field
    has_description = False
    for field_name in custom_fields:
        if field_name in ["Beschrijf", "Persoonlijk verhaal", "Vertel iets over deze persoon", "Toelichting", 
                         "Vertel over de gelegenheid", "Vertel over de persoon", "Vertel over deze persoon",
                         "Vertel over je wensen", "Vertel over je ideeën", "Vertel je verhaal", "Vertel meer", "Vertel"]:
            has_description = True
            logger.info(f"Order {order_id}: Found description field '{field_name}'")
            break
    
    # Step 6: If no description found, try alternative fields
    if not has_description:
        # Try fields that might contain descriptions
        for field_name, field_value in custom_fields.items():
            if any(keyword in field_name.lower() for keyword in ["opmerking", "notitie", "wens", "idee", "verhaal", "vertel", "beschrijf"]):
                custom_fields["Beschrijf"] = field_value
                logger.info(f"Order {order_id}: Found description in alternative field '{field_name}'")
                has_description = True
                break
        
        # If still no description, create a composite one
        if not has_description:
            description_parts = []
            if "Thema" in custom_fields:
                description_parts.append(f"Thema: {custom_fields['Thema']}")
            if "Gelegenheid" in custom_fields:
                description_parts.append(f"Gelegenheid: {custom_fields['Gelegenheid']}")
            if "Toon" in custom_fields:
                description_parts.append(f"Gewenste toon: {custom_fields['Toon']}")
            
            if description_parts:
                custom_fields["Beschrijf"] = "\n".join(description_parts)
                logger.info(f"Order {order_id}: Created composite description from {len(description_parts)} fields")
                has_description = True
    
    return custom_fields

def map_custom_fields_to_order(custom_fields, order_id):
    """
    Map custom fields to order attributes, simulating the logic in orders.py
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
    
    # Log summary of found fields before mapping
    logger.info(f"Order {order_id}: Found {len(custom_fields)} custom fields in total: {', '.join(custom_fields.keys())}")
    
    # Map custom fields to order attributes
    mapped_fields = 0
    for field_name, field_value in custom_fields.items():
        # Check if this field is in our mapping
        if field_name in field_mapping:
            attr_name = field_mapping[field_name]
            order[attr_name] = field_value
            mapped_fields += 1
            logger.info(f"Order {order_id}: Custom field '{field_name}' mapped to '{attr_name}'")
    
    # Log result
    logger.info(f"Order {order_id}: {mapped_fields} custom fields mapped to order attributes")
    
    # Final verification for critical fields
    if "beschrijving" in order and order["beschrijving"]:
        desc_length = len(order["beschrijving"])
        logger.info(f"Order {order_id}: Final beschrijving field has {desc_length} characters")
        logger.info(f"Order {order_id}: Content preview: {order['beschrijving'][:100]}..." if desc_length > 100 else order['beschrijving'])
    else:
        logger.warning(f"Order {order_id}: No beschrijving field was mapped or it's empty")
    
    return order

def test_order_processing(order_data):
    """Test the processing of an order"""
    order_id = order_data.get("order_id", "unknown")
    logger.info(f"=== Testing order {order_id} ===")
    
    # Extract custom fields
    custom_fields = extract_custom_fields(order_data)
    
    # Map custom fields to order
    order = map_custom_fields_to_order(custom_fields, order_id)
    
    # Print the final order object
    logger.info(f"=== Final order object for {order_id} ===")
    for key, value in order.items():
        if key == "beschrijving" and value:
            logger.info(f"{key}: {value[:50]}... ({len(value)} chars)")
        else:
            logger.info(f"{key}: {value}")
    
    logger.info(f"=== End of test for order {order_id} ===\n")
    return order

if __name__ == "__main__":
    logger.info("Starting description extraction tests")
    
    # Test with product-level description
    logger.info("\n=== TEST 1: Order with product-level description ===")
    order1 = test_order_processing(sample_order)
    
    # Test with address.note description
    logger.info("\n=== TEST 2: Order with address.note description ===")
    order2 = test_order_processing(sample_order_with_note)
    
    # Test with no description
    logger.info("\n=== TEST 3: Order with no description fields ===")
    order3 = test_order_processing(sample_order_no_description)
    
    # Test with old format custom fields
    logger.info("\n=== TEST 4: Order with old format custom fields ===")
    order4 = test_order_processing(sample_order_old_format)
    
    # Test with description in alternative field
    logger.info("\n=== TEST 5: Order with description in alternative field ===")
    order5 = test_order_processing(sample_order_alt_description)
    
    logger.info("All tests completed")
