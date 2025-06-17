"""
Orders Router

Deze module bevat API endpoints voor het beheren van bestellingen.
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, Path
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.order import Order
from app.schemas.order import OrderRead
from app.services.plugpay_client import fetch_and_store_recent_orders, PlugPayAPIError
from app.auth.token import get_api_key
from app.crud import order as crud

# Configureer logging
logger = logging.getLogger(__name__)

# Schema voor raw data response
class RawDataResponse(BaseModel):
    """Schema voor het tonen van raw data."""
    raw_data: Optional[Dict[str, Any]] = None

router = APIRouter(
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@router.options("/fetch")
async def options_fetch():
    """
    Explicit OPTIONS handler for CORS preflight requests.
    Returns a 200 OK response with appropriate CORS headers.
    """
    response = Response(status_code=200)
    return response

@router.options("/orders")
async def options_orders():
    """
    Explicit OPTIONS handler for CORS preflight requests to /orders.
    Returns a 200 OK response with appropriate CORS headers.
    """
    response = Response(status_code=200)
    return response

@router.options("/orders/orders")
async def options_orders_orders():
    """
    Explicit OPTIONS handler for CORS preflight requests to /orders/orders.
    Returns a 200 OK response with appropriate CORS headers.
    """
    response = Response(status_code=200)
    return response

@router.options("/{order_id}")
async def options_order_detail():
    """
    Explicit OPTIONS handler for CORS preflight requests to /orders/{order_id}.
    Returns a 200 OK response with appropriate CORS headers.
    """
    response = Response(status_code=200)
    return response

@router.get("/orders", response_model=List[OrderRead])
async def get_all_orders(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Haalt alle bestellingen op uit de database.
    
    Vereist API-key authenticatie.
    
    Returns:
        Een lijst van alle bestellingen
    """
    try:
        orders = db.query(Order).all()
        return orders
    except Exception as e:
        logger.error(f"Fout bij ophalen van bestellingen: {str(e)}")
        raise HTTPException(status_code=500, detail="Er is een fout opgetreden bij het ophalen van bestellingen")

@router.get("/orders/orders", response_model=List[OrderRead])
async def get_all_orders_nested(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Haalt alle bestellingen op uit de database (geneste route).
    
    Vereist API-key authenticatie.
    
    Returns:
        Een lijst van alle bestellingen
    """
    try:
        orders = db.query(Order).all()
        return orders
    except Exception as e:
        logger.error(f"Fout bij ophalen van bestellingen (geneste route): {str(e)}")
        raise HTTPException(status_code=500, detail="Er is een fout opgetreden bij het ophalen van bestellingen")

@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int = Path(..., description="Plug&Pay order_id"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(get_api_key),
):
    """
    Haalt een specifieke bestelling op uit de database op basis van het ID.
    
    Vereist API-key authenticatie.
    
    Args:
        order_id: ID van de bestelling
        db: Database sessie
        x_api_key: API key voor authenticatie
        
    Returns:
        De opgevraagde bestelling met alle custom fields
        
    Raises:
        HTTPException: Als de bestelling niet gevonden wordt (404)
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order niet gevonden")
    
    # Voeg custom fields toe aan het order object voor de frontend
    # Deze functie verwerkt zowel oude (name/value) als nieuwe (label/input) formats
    if order.raw_data:
        # Dictionary om custom fields op te slaan
        custom_fields = {}
        logger.info(f"Order {order_id}: Starting extraction of custom fields")
        
        # Try to extract from root-level custom_field_inputs (new format)
        if "custom_field_inputs" in order.raw_data and order.raw_data["custom_field_inputs"]:
            for field in order.raw_data["custom_field_inputs"]:
                if "label" in field and ("input" in field or "value" in field):
                    label = field.get("label", "onbekend")
                    value = field.get("input") or field.get("value")

                    if value is not None:
                        custom_fields[label] = value
                    else:
                        logger.warning(f"Order {order_id}: Custom field zonder waarde aangetroffen: {field}")
                    logger.info(f"Order {order_id}: Found field '{field.get('label', 'onbekend')}' in root-level custom_field_inputs")
                else:
                    logger.warning(f"Order {order_id}: Ongeldig custom field formaat: {field}")
        
        # Try to extract from root-level custom_fields (old format)
        if "custom_fields" in order.raw_data and order.raw_data["custom_fields"]:
            raw_custom_fields = order.raw_data["custom_fields"]
            
            # Handle both dict and list formats for custom_fields
            if isinstance(raw_custom_fields, dict):
                # Process as key-value pairs (original format)
                for field_name, field_value in raw_custom_fields.items():
                    custom_fields[field_name] = field_value
                    logger.info(f"Order {order_id}: Found field '{field_name}' in root-level custom_fields (dict format)")
            elif isinstance(raw_custom_fields, list):
                # Process as list of dicts with name/label and value/input/text
                for field in raw_custom_fields:
                    try:
                        field_name = field.get("label") or field.get("name", "onbekend")
                        field_value = field.get("input") or field.get("value") or field.get("text") or ""
                        if not field_value:
                            logger.warning(f"Order {order_id}: Ongeldig custom field zonder waarde: {field}")
                            continue
                        custom_fields[field_name] = field_value
                        logger.info(f"Order {order_id}: Found field '{field_name}' in root-level custom_fields (list format)")
                    except Exception as e:
                        logger.warning(f"Order {order_id}: Ongeldig custom field formaat: {field}, error: {str(e)}")
            else:
                logger.warning(f"Order {order_id}: Onbekend formaat voor custom_fields: {type(raw_custom_fields)}")
        
        # Extract product-level custom fields
        product_fields_found = False
        if "products" in order.raw_data and order.raw_data["products"]:
            logger.info(f"Order {order_id}: Found {len(order.raw_data['products'])} products to check for custom fields")
            for product_idx, product in enumerate(order.raw_data["products"]):
                # Try new format (custom_field_inputs)
                if "custom_field_inputs" in product and product["custom_field_inputs"]:
                    logger.info(f"Order {order_id}: Product {product_idx} has {len(product['custom_field_inputs'])} custom_field_inputs")
                    for field in product["custom_field_inputs"]:
                        if "label" in field and ("input" in field or "value" in field):
                            label = field.get("label", "onbekend")
                            value = field.get("input") or field.get("value")

                            if value is not None:
                                custom_fields[label] = value
                                product_fields_found = True
                                logger.info(f"Order {order_id}: Found field '{label}' in product-level custom_field_inputs")
                            else:
                                logger.warning(f"Order {order_id}: Custom field zonder waarde aangetroffen in product: {field}")
                            # product_fields_found en logging worden nu in de bovenstaande code afgehandeld
                            # Log the content length for description fields to help diagnose issues
                            if field.get('label') in ['Beschrijf', 'Persoonlijk verhaal', 'Vertel over de gelegenheid']:
                                value = field.get('input') or field.get('value')
                                content_length = len(value) if value is not None else 0
                                logger.info(f"Order {order_id}: Field '{field.get('label', 'onbekend')}' has content length of {content_length} characters")
                        else:
                            logger.warning(f"Order {order_id}: Ongeldig custom field formaat in product: {field}")
                
                # Try old format (custom_fields)
                if "custom_fields" in product and product["custom_fields"]:
                    logger.info(f"Order {order_id}: Product {product_idx} has custom_fields (old format)")
                    for field_name, field_value in product["custom_fields"].items():
                        custom_fields[field_name] = field_value
                        product_fields_found = True
                        logger.info(f"Order {order_id}: Found field '{field_name}' in product-level custom_fields")
        
        # Check if any product-level fields were found
        if product_fields_found:
            logger.info(f"Order {order_id}: Successfully found custom fields in products")
        else:
            logger.info(f"Order {order_id}: No custom fields found in products")
        
        # Voeg persoonlijk verhaal toe uit address.note als het bestaat
        if "address" in order.raw_data and order.raw_data["address"] and "note" in order.raw_data["address"]:
            note = order.raw_data["address"]["note"]
            if note and len(note.strip()) > 0:
                custom_fields["Beschrijf"] = note
                logger.info(f"Order {order_id}: Persoonlijk verhaal gevonden in address.note met lengte {len(note)}")
        
        # Controleer of er een beschrijving is gevonden, zo niet, probeer andere velden
        has_description = False
        for field_name in custom_fields:
            if field_name in ["Beschrijf", "Persoonlijk verhaal", "Vertel iets over deze persoon", "Toelichting", 
                             "Vertel over de gelegenheid", "Vertel over de persoon", "Vertel over deze persoon",
                             "Vertel over je wensen", "Vertel over je ideeën", "Vertel je verhaal", "Vertel meer", "Vertel"]:
                has_description = True
                break
        
        # Als er geen beschrijving is gevonden, probeer andere velden te gebruiken als fallback
        if not has_description:
            # Probeer opmerkingen of notities velden
            for field_name, field_value in custom_fields.items():
                # Zoek naar velden die mogelijk beschrijvingen bevatten
                if any(keyword in field_name.lower() for keyword in ["opmerking", "notitie", "wens", "idee", "verhaal", "vertel", "beschrijf"]):
                    custom_fields["Beschrijf"] = field_value
                    logger.info(f"Order {order_id}: Beschrijving gevonden in alternatief veld '{field_name}'")
                    has_description = True
                    break
            
            # Als er nog steeds geen beschrijving is, probeer een samengestelde beschrijving te maken
            if not has_description:
                description_parts = []
                # Voeg relevante velden samen om een beschrijving te maken
                if "Thema" in custom_fields:
                    description_parts.append(f"Thema: {custom_fields['Thema']}")
                if "Gelegenheid" in custom_fields:
                    description_parts.append(f"Gelegenheid: {custom_fields['Gelegenheid']}")
                if "Toon" in custom_fields:
                    description_parts.append(f"Gewenste toon: {custom_fields['Toon']}")
                
                if description_parts:
                    custom_fields["Beschrijf"] = "\n".join(description_parts)
                    logger.info(f"Order {order_id}: Samengestelde beschrijving gemaakt uit {len(description_parts)} velden")
        
        # Map custom fields naar specifieke velden in het order object
        # Gebruik een mapping van mogelijke veldnamen naar attributen
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
        
        # Wijs custom fields toe aan order attributen
        mapped_fields = 0
        for field_name, field_value in custom_fields.items():
            # Check of dit veld in onze mapping staat
            if field_name in field_mapping:
                attr_name = field_mapping[field_name]
                setattr(order, attr_name, field_value)
                mapped_fields += 1
                logger.info(f"Order {order_id}: Custom field '{field_name}' toegewezen aan '{attr_name}'")
        
        # Log resultaat
        logger.info(f"Order {order_id}: {len(custom_fields)} custom fields verwerkt")
        
        # Final verification for critical fields
        if hasattr(order, 'beschrijving') and order.beschrijving:
            desc_length = len(order.beschrijving)
            logger.info(f"Order {order_id}: Final beschrijving field has {desc_length} characters")
        else:
            logger.warning(f"Order {order_id}: No beschrijving field was mapped or it's empty")
    
    return order

@router.post("/fetch")
async def fetch_orders(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Haalt recente bestellingen op van Plug&Pay en slaat ze op in de database.
    Deze taak wordt op de achtergrond uitgevoerd.
    
    Vereist API-key authenticatie.
    
    Returns:
        Een JSON-response met een bevestiging en het resultaat
    """
    try:
        # Voer de taak uit en haal het resultaat op
        new_orders, skipped_orders = fetch_and_store_recent_orders(db)
        
        # Stuur een bevestiging terug met het resultaat
        return {
            "message": "Orders fetched",
            "result": {
                "new_orders": new_orders,
                "skipped_orders": skipped_orders
            }
        }
    except PlugPayAPIError as e:
        logger.error(f"Fout bij ophalen van bestellingen: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Onverwachte fout bij ophalen van bestellingen: {str(e)}")
        raise HTTPException(status_code=500, detail="Er is een fout opgetreden bij het ophalen van bestellingen")

@router.get("/raw-data/{order_id}", response_model=RawDataResponse)
def get_order_raw_data(
    order_id: int = Path(..., description="Plug&Pay order_id"),
    db: Session = Depends(get_db),
    x_api_key: str = Depends(get_api_key),
):
    """
    Haalt alleen de raw_data van een specifieke bestelling op.
    
    Vereist API-key authenticatie.
    
    Args:
        order_id: ID van de bestelling
        db: Database sessie
        x_api_key: API key voor authenticatie
        
    Returns:
        De raw_data van de opgevraagde bestelling
        
    Raises:
        HTTPException: Als de bestelling niet gevonden wordt (404)
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order niet gevonden")
    return {"raw_data": order.raw_data}
