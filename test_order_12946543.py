"""
Test script to diagnose why order #12946543 description is not showing in the UI.
This script will:
1. Fetch the order from the database
2. Extract and log all custom fields
3. Verify the mapping of description fields
4. Check if the final order object has the description field set
"""

import logging
import sys
import json
import os

# Set the DATABASE_URL environment variable before importing any app modules
os.environ["DATABASE_URL"] = "postgresql://song_scribe_db_user:EHoXvsQYuo72p2mKNhcrbJZYmVOBzw8D@dpg-d10nt6i4d50c73b0doq0-a/song_scribe_db"

# Configure logging to output to console
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("order_diagnosis")

# Import SQLAlchemy after setting environment variable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import app modules (adjust path if needed)
from app.models.order import Order
from app.schemas.order import OrderRead
from app.routers.orders import read_order

# Create a database connection
try:
    # Use the DATABASE_URL from environment variable
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    logger.info(f"Connected to database: {database_url}")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    sys.exit(1)

def diagnose_order(order_id: int):
    """Diagnose why an order's description is not showing in the UI"""
    logger.info(f"Starting diagnosis for order #{order_id}")
    
    # Step 1: Get the order from the database
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            logger.error(f"Order #{order_id} not found in database")
            return
        logger.info(f"Order #{order_id} found in database")
    except Exception as e:
        logger.error(f"Error fetching order from database: {str(e)}")
        return
    
    # Step 2: Check if raw_data exists and has the expected structure
    if not order.raw_data:
        logger.error(f"Order #{order_id} has no raw_data")
        return
    
    logger.info(f"Order #{order_id} raw_data keys: {', '.join(order.raw_data.keys())}")
    
    # Step 3: Extract custom fields from raw_data
    custom_fields = {}
    
    # Try to extract from root-level custom_field_inputs (new format)
    if "custom_field_inputs" in order.raw_data and order.raw_data["custom_field_inputs"]:
        logger.info(f"Order has {len(order.raw_data['custom_field_inputs'])} root-level custom_field_inputs")
        for field in order.raw_data["custom_field_inputs"]:
            custom_fields[field["label"]] = field["input"]
            logger.info(f"Found field '{field['label']}' in root-level custom_field_inputs")
    else:
        logger.warning("No root-level custom_field_inputs found")
    
    # Try to extract from root-level custom_fields (old format)
    if "custom_fields" in order.raw_data and order.raw_data["custom_fields"]:
        logger.info(f"Order has root-level custom_fields (old format)")
        for field_name, field_value in order.raw_data["custom_fields"].items():
            custom_fields[field_name] = field_value
            logger.info(f"Found field '{field_name}' in root-level custom_fields")
    else:
        logger.warning("No root-level custom_fields found")
    
    # Extract product-level custom fields
    product_fields_found = False
    if "products" in order.raw_data and order.raw_data["products"]:
        logger.info(f"Order has {len(order.raw_data['products'])} products")
        for product_idx, product in enumerate(order.raw_data["products"]):
            logger.info(f"Checking product {product_idx}")
            
            # Try new format (custom_field_inputs)
            if "custom_field_inputs" in product and product["custom_field_inputs"]:
                logger.info(f"Product {product_idx} has {len(product['custom_field_inputs'])} custom_field_inputs")
                for field in product["custom_field_inputs"]:
                    custom_fields[field["label"]] = field["input"]
                    product_fields_found = True
                    logger.info(f"Found field '{field['label']}' in product-level custom_field_inputs")
                    
                    # Log the content length for description fields
                    if field["label"] in ["Beschrijf", "Persoonlijk verhaal", "Vertel over de gelegenheid"]:
                        content_length = len(field["input"]) if field["input"] else 0
                        logger.info(f"Description field '{field['label']}' has content length of {content_length} characters")
                        logger.info(f"Content preview: {field['input'][:100]}..." if field["input"] else "Empty content")
            
            # Try old format (custom_fields)
            if "custom_fields" in product and product["custom_fields"]:
                logger.info(f"Product {product_idx} has custom_fields (old format)")
                for field_name, field_value in product["custom_fields"].items():
                    custom_fields[field_name] = field_value
                    product_fields_found = True
                    logger.info(f"Found field '{field_name}' in product-level custom_fields")
    else:
        logger.warning("No products found in order data")
    
    # Check if address note is present
    if "address" in order.raw_data and order.raw_data["address"] and "note" in order.raw_data["address"]:
        note = order.raw_data["address"]["note"]
        if note and len(note.strip()) > 0:
            custom_fields["Beschrijf"] = note
            logger.info(f"Found personal story in address.note with length {len(note)}")
        else:
            logger.info("address.note is empty or only whitespace")
    else:
        logger.info("No address.note found")
    
    # Step 4: Map custom fields to order attributes
    logger.info(f"Found {len(custom_fields)} custom fields in total: {', '.join(custom_fields.keys())}")
    
    # Define the field mapping (same as in orders.py)
    field_mapping = {
        # Description variants
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
    
    # Check if any description fields are present
    description_fields = [field for field in custom_fields.keys() if field in field_mapping and field_mapping[field] == "beschrijving"]
    if description_fields:
        logger.info(f"Found description fields: {', '.join(description_fields)}")
        for field in description_fields:
            content_length = len(custom_fields[field]) if custom_fields[field] else 0
            logger.info(f"Field '{field}' has content length of {content_length} characters")
    else:
        logger.warning("No description fields found in custom fields")
    
    # Step 5: Test the read_order function
    try:
        logger.info("Testing read_order function...")
        processed_order = read_order(order_id, db, "test_api_key")
        
        if hasattr(processed_order, 'beschrijving') and processed_order.beschrijving:
            logger.info(f"SUCCESS: beschrijving field is set with {len(processed_order.beschrijving)} characters")
            logger.info(f"Preview: {processed_order.beschrijving[:100]}...")
        else:
            logger.error("FAILURE: beschrijving field is not set after processing")
            
        # Convert order to dict for inspection
        order_dict = processed_order.__dict__
        logger.info(f"Order attributes: {', '.join([k for k in order_dict.keys() if not k.startswith('_')])}")
        
    except Exception as e:
        logger.error(f"Error testing read_order function: {str(e)}")
    
    # Step 6: Check if the order is properly serialized to OrderRead schema
    try:
        logger.info("Testing OrderRead schema serialization...")
        order_read = OrderRead.from_orm(processed_order)
        order_json = order_read.json()
        order_dict = json.loads(order_json)
        
        if "beschrijving" in order_dict and order_dict["beschrijving"]:
            logger.info(f"SUCCESS: beschrijving is present in OrderRead schema with {len(order_dict['beschrijving'])} characters")
        else:
            logger.error("FAILURE: beschrijving is missing or empty in OrderRead schema")
            
    except Exception as e:
        logger.error(f"Error testing OrderRead schema: {str(e)}")

if __name__ == "__main__":
    # Test for the specific order ID
    diagnose_order(12946543)
    logger.info("Diagnosis complete")
