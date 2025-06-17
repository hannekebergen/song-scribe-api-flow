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
        
        # Functie om custom fields te extraheren uit verschillende formaten
        def extract_custom_fields(fields_array, field_format="old"):
            if not isinstance(fields_array, list):
                return {}
                
            extracted = {}
            for field in fields_array:
                if not isinstance(field, dict):
                    continue
                    
                # Oude format: name/value
                if field_format == "old" and "name" in field and "value" in field:
                    extracted[field["name"]] = field["value"]
                # Nieuwe format: label/input
                elif field_format == "new" and "label" in field and "input" in field:
                    extracted[field["label"]] = field["input"]
                    
            return extracted
        
        # Probeer custom_field_inputs (oude format)
        if "custom_field_inputs" in order.raw_data:
            old_format = extract_custom_fields(order.raw_data["custom_field_inputs"], "old")
            custom_fields.update(old_format)
        
        # Probeer custom_fields (nieuwe format)
        if "custom_fields" in order.raw_data:
            new_format = extract_custom_fields(order.raw_data["custom_fields"], "new")
            custom_fields.update(new_format)
            
        # Probeer product-level custom fields
        if "products" in order.raw_data and isinstance(order.raw_data["products"], list):
            for product in order.raw_data["products"]:
                # Oude format in product
                if "custom_field_inputs" in product:
                    product_old = extract_custom_fields(product["custom_field_inputs"], "old")
                    custom_fields.update(product_old)
                    
                # Nieuwe format in product
                if "custom_fields" in product:
                    product_new = extract_custom_fields(product["custom_fields"], "new")
                    custom_fields.update(product_new)
        
        # Voeg persoonlijk verhaal toe uit address.note als het bestaat
        if "address" in order.raw_data and order.raw_data["address"] and "note" in order.raw_data["address"]:
            note = order.raw_data["address"]["note"]
            if note and len(note.strip()) > 0:
                custom_fields["Beschrijf"] = note
        
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
        }
        
        # Wijs custom fields toe aan order attributen
        for field_name, field_value in custom_fields.items():
            # Check of dit veld in onze mapping staat
            if field_name in field_mapping:
                attr_name = field_mapping[field_name]
                setattr(order, attr_name, field_value)
                logger.debug(f"Order {order_id}: Custom field '{field_name}' toegewezen aan '{attr_name}'")
        
        # Log resultaat
        logger.info(f"Order {order_id}: {len(custom_fields)} custom fields verwerkt")
    
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
