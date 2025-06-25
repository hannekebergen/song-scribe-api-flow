"""
Orders Router

Deze module bevat API endpoints voor het beheren van bestellingen.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, Path
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc as sa_exc
from pydantic import BaseModel, ValidationError

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

# Schema voor update response
class UpdateResponse(BaseModel):
    """Schema voor update response."""
    message: str
    updated_count: int
    total_processed: int

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
        orders = db.query(Order).order_by(Order.bestel_datum.desc()).all()
        safe_orders = []
        skipped = 0
        for o in orders:
            try:
                safe_orders.append(OrderRead.model_validate(o).model_dump(mode='json'))
            except ValidationError as ve:
                skipped += 1
                logger.warning(f"Order {o.id} overgeslagen door schema-fout: {str(ve)}")
        logger.info(f"Total {len(safe_orders)} orders ok, {skipped} skipped")
        return JSONResponse(
            content=safe_orders,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except sa_exc.ProgrammingError as pe:
        error_msg = str(pe)
        if ("column orders.thema does not exist" in error_msg or 
            "column orders.persoonlijk_verhaal does not exist" in error_msg or 
            "UndefinedColumn" in str(pe.__class__)):
            logger.error("DB-kolom ontbreekt – heeft migration al gedraaid? %s", pe)
            return JSONResponse(
                status_code=500,
                content={"detail": "Database-schema niet up-to-date. Voer de Alembic migratie uit."},
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        raise
    except Exception as e:
        logger.error(f"Fout bij ophalen van bestellingen: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Er is een fout opgetreden bij het ophalen van bestellingen"},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@router.get("/orders/orders", response_model=List[OrderRead])
async def get_all_orders_nested(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Haalt alle bestellingen op uit de database (geneste route).
    
    Vereist API-key authenticatie.
    
    Returns:
        Een lijst van alle bestellingen
    """
    try:
        orders = db.query(Order).order_by(Order.bestel_datum.desc()).all()
        safe_orders = []
        skipped = 0
        for o in orders:
            try:
                safe_orders.append(OrderRead.model_validate(o).model_dump(mode='json'))
            except ValidationError as ve:
                skipped += 1
                logger.warning(f"Order {o.id} overgeslagen door schema-fout: {str(ve)}")
        logger.info(f"Total {len(safe_orders)} orders ok, {skipped} skipped")
        return JSONResponse(
            content=safe_orders,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except sa_exc.ProgrammingError as pe:
        error_msg = str(pe)
        if ("column orders.thema does not exist" in error_msg or 
            "column orders.persoonlijk_verhaal does not exist" in error_msg or 
            "UndefinedColumn" in str(pe.__class__)):
            logger.error("DB-kolom ontbreekt – heeft migration al gedraaid? %s", pe)
            return JSONResponse(
                status_code=500,
                content={"detail": "Database-schema niet up-to-date. Voer de Alembic migratie uit."},
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        raise
    except Exception as e:
        logger.error(f"Fout bij ophalen van bestellingen (geneste route): {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Er is een fout opgetreden bij het ophalen van bestellingen"},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

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
        De opgevraagde bestelling
        
    Raises:
        HTTPException: Als de bestelling niet gevonden wordt (404)
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order niet gevonden")
    
    # Controleer of de order custom fields heeft
    if order.raw_data and "custom_field_inputs" in order.raw_data:
        custom_fields = {}
        
        # Verzamel alle custom fields uit de raw_data
        for field in order.raw_data["custom_field_inputs"]:
            if "name" in field and "value" in field:
                custom_fields[field["name"]] = field["value"]
        
        # Mapping van custom field namen naar order attributen
        field_mapping = {
            # Voornaam varianten
            "Voornaam": "voornaam",
            "Naam": "voornaam",
            "Voor wie is dit lied?": "voornaam",
            
            # Achternaam varianten
            "Achternaam": "van",
            "Van": "van",
            
            # Relatie varianten
            "Relatie": "relatie",
            "Wat is je relatie tot deze persoon?": "relatie",
            "Hoe ken je deze persoon?": "relatie",
            
            # Datum varianten
            "Datum": "datum",
            "Wanneer": "datum",
            "Wanneer is de gelegenheid?": "datum",
            "Wanneer moet het lied klaar zijn?": "datum",
            
            # Thema varianten
            "Thema": "thema",
            "Gelegenheid": "thema",
            "Voor welke gelegenheid": "thema",
            "Voor welke gelegenheid?": "thema",
            "Waarvoor is dit lied?": "thema",
            "Vertel over de gelegenheid": "thema",
            
            # Toon varianten
            "Toon": "toon",
            "Gewenste stijl": "toon",
            "Stijl": "toon",
            "Sfeer": "toon",
            
            # Structuur varianten
            "Structuur": "structuur",
            "Opbouw": "structuur",
            
            # Rijm varianten
            "Rijm": "rijm",
            "Rijmschema": "rijm",
            
            # Beschrijving varianten
            "Beschrijf": "beschrijving",
            "Toelichting": "beschrijving",
            "Vertel over de persoon": "beschrijving",
            "Vertel over deze persoon": "beschrijving",
            "Vertel over je wensen": "beschrijving",
            "Vertel over je ideeën": "beschrijving",
            "Vertel je verhaal": "beschrijving",
            "Vertel meer": "beschrijving",
            "Vertel": "beschrijving",
            
            # Persoonlijk verhaal varianten (mapped to beschrijving)
            "Persoonlijk verhaal": "beschrijving",
            "Vertel iets over deze persoon": "beschrijving",
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
    
    return JSONResponse(
        content=OrderRead.model_validate(order).model_dump(mode='json'),
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

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
        return JSONResponse(
            content={
                "message": "Orders fetched",
                "result": {
                    "new_orders": new_orders,
                    "skipped_orders": skipped_orders
                }
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except PlugPayAPIError as e:
        logger.error(f"Fout bij ophalen van bestellingen: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        logger.error(f"Onverwachte fout bij ophalen van bestellingen: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Er is een fout opgetreden bij het ophalen van bestellingen"},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

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
        return JSONResponse(
            status_code=404,
            content={"detail": "Order niet gevonden"},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    return JSONResponse(
        content={"raw_data": order.raw_data},
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@router.post("/update-names", response_model=UpdateResponse)
async def update_order_names(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Update bestaande orders met verbeterde klantnaam extractie.
    
    Vereist API-key authenticatie.
    
    Returns:
        UpdateResponse met aantal bijgewerkte orders
    """
    try:
        # Get all orders
        orders = db.query(Order).all()
        logger.info(f"Found {len(orders)} orders to process")
        
        updated_count = 0
        
        for order in orders:
            if not order.raw_data:
                logger.warning(f"Order {order.order_id} has no raw_data, skipping")
                continue
            
            # Extract improved name using the new logic
            customer = order.raw_data.get("customer", {})
            
            # Custom fields extractie (try both locations)
            custom = {}
            
            # Check root level custom_field_inputs
            custom_field_inputs = order.raw_data.get("custom_field_inputs", [])
            for field in custom_field_inputs:
                name = field.get("name") or field.get("label")
                value = field.get("value") or field.get("input")
                if name and value:
                    custom[name] = value
            
            # Check products level custom_field_inputs
            products = order.raw_data.get("products", [])
            for product in products:
                product_custom_fields = product.get("custom_field_inputs", [])
                for field in product_custom_fields:
                    name = field.get("name") or field.get("label")
                    value = field.get("value") or field.get("input")
                    if name and value:
                        custom[name] = value
            
            def pick(*keys):
                for k in keys:
                    if k in custom:
                        return custom[k]
                return None
            
            # Verbeterde klantnaam extractie (6-staps systeem)
            def get_klant_naam():
                # Stap 1: Address full_name
                address = order.raw_data.get("address", {})
                if address.get("full_name"):
                    return address.get("full_name")
                
                # Stap 2: Address firstname + lastname
                if address.get("firstname"):
                    firstname = address.get("firstname")
                    lastname = address.get("lastname", "")
                    return f"{firstname} {lastname}".strip()
                
                # Stap 3: Customer name
                if customer.get("name"):
                    return customer.get("name")
                
                # Stap 4: Custom fields (uitgebreide lijst)
                name_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
                    "Voor wie is het lied?", "Wie is de ontvanger?", 
                    "Naam ontvanger", "Klant naam"
                ]
                for field_name in name_fields:
                    value = pick(field_name)
                    if value:
                        # Probeer ook achternaam toe te voegen
                        achternaam = pick("Achternaam", "Van")
                        if achternaam:
                            return f"{value} {achternaam}"
                        return value
                
                # Stap 5: Name extraction from description (basic regex)
                description = order.raw_data.get("description", "")
                if description:
                    # Zoek naar patronen zoals "voor [naam]" of "aan [naam]"
                    patterns = [
                        r"voor\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
                        r"aan\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
                        r"van\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)"
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, description, re.IGNORECASE)
                        if match:
                            return match.group(1).strip()
                
                return None
            
            new_klant_naam = get_klant_naam()
            
            # Update als er een verbetering is
            if new_klant_naam and new_klant_naam != order.klant_naam:
                old_name = order.klant_naam or "None"
                order.klant_naam = new_klant_naam
                logger.info(f"Order {order.order_id}: Updated klant_naam from '{old_name}' to '{new_klant_naam}'")
                updated_count += 1
            
            # Update voornaam field for better frontend display (4-staps systeem)
            def get_voornaam():
                # Stap 1: Address firstname
                address = order.raw_data.get("address", {})
                if address.get("firstname"):
                    return address.get("firstname")
                
                # Stap 2: Custom fields (uitgebreide lijst)
                voornaam_fields = [
                    "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
                    "Voor wie is het lied?", "Wie is de ontvanger?", 
                    "Naam ontvanger"
                ]
                for field_name in voornaam_fields:
                    value = pick(field_name)
                    if value:
                        return value.split()[0]  # First word only for voornaam
                
                # Stap 3: Customer name (first word)
                if customer.get("name"):
                    return customer.get("name").split()[0]
                
                # Stap 4: Address full_name (first word)
                if address.get("full_name"):
                    return address.get("full_name").split()[0]
                
                return None
            
            new_voornaam = get_voornaam()
            
            if new_voornaam and new_voornaam != order.voornaam:
                old_voornaam = order.voornaam or "None"
                order.voornaam = new_voornaam
                logger.info(f"Order {order.order_id}: Updated voornaam from '{old_voornaam}' to '{new_voornaam}'")
                updated_count += 1
        
        # Commit changes
        if updated_count > 0:
            db.commit()
            logger.info(f"Successfully updated {updated_count} orders")
        else:
            logger.info("No orders needed updating")
        
        return UpdateResponse(
            message=f"Successfully processed {len(orders)} orders",
            updated_count=updated_count,
            total_processed=len(orders)
        )
        
    except Exception as e:
        logger.error(f"Error updating orders: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating orders: {str(e)}"
        )
