"""
Orders Router

Deze module bevat API endpoints voor het beheren van bestellingen.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, Path, Body
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc as sa_exc
from pydantic import BaseModel, ValidationError, Field

from app.db.session import get_db
from app.models.order import Order
from app.schemas.order import OrderRead, UpdateSongtextRequest
from app.services.plugpay_client import fetch_and_store_recent_orders, PlugPayAPIError
from app.auth.token import get_api_key
from app.crud import order as crud
from app.services.upsell_linking import find_original_order_for_upsell, inherit_theme_from_original

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
            
            # Temporarily disabled until voornaam column is added to database
            # new_voornaam = get_voornaam()
            # 
            # if new_voornaam and new_voornaam != order.voornaam:
            #     old_voornaam = order.voornaam or "None"
            #     order.voornaam = new_voornaam
            #     logger.info(f"Order {order.order_id}: Updated voornaam from '{old_voornaam}' to '{new_voornaam}'")
            #     updated_count += 1
        
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

@router.post("/link-upsell-orders", response_model=UpdateResponse)
async def link_upsell_orders(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Link bestaande UpSell orders aan hun originele orders en neem thema's over.
    """
    try:
        # Haal alle UpSell orders op die nog niet gelinkt zijn
        upsell_orders = db.query(Order).filter(
            Order.origin_song_id.is_(None)  # Nog niet gelinkt
        ).all()
        
        linked_count = 0
        theme_inherited_count = 0
        
        for order in upsell_orders:
            # Check of dit een UpSell order is
            is_upsell = False
            if order.raw_data and order.raw_data.get("products"):
                for product in order.raw_data["products"]:
                    pivot_type = product.get("pivot", {}).get("type")
                    if pivot_type == "upsell":
                        is_upsell = True
                        break
            
            if is_upsell:
                # Probeer originele order te vinden
                original_order_id = find_original_order_for_upsell(db, order.raw_data)
                
                if original_order_id:
                    order.origin_song_id = original_order_id
                    linked_count += 1
                    
                    # Probeer thema over te nemen als de UpSell order geen thema heeft
                    if not order.thema or order.thema == '-' or order.thema == 'Onbekend':
                        if inherit_theme_from_original(db, order, original_order_id):
                            theme_inherited_count += 1
                    
                    logger.info(f"UpSell order {order.order_id} gelinkt aan originele order {original_order_id}")
        
        # Commit alle wijzigingen
        db.commit()
        
        return UpdateResponse(
            message=f"UpSell linking voltooid: {linked_count} orders gelinkt, {theme_inherited_count} thema's overgenomen",
            updated_count=linked_count,
            total_processed=len(upsell_orders)
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Fout bij linken van UpSell orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fout bij linken van UpSell orders: {str(e)}")

@router.get("/{order_id}/original-songtext")
async def get_original_songtext(
    order_id: int = Path(..., description="Upsell order ID"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Haalt de originele songtekst op voor een upsell order.
    
    Voor upsell orders die gelinkt zijn aan een originele order via origin_song_id,
    wordt de songtekst van die originele order opgehaald.
    
    Args:
        order_id: ID van de upsell order
        db: Database sessie
        api_key: API key voor authenticatie
        
    Returns:
        De originele songtekst en order informatie
        
    Raises:
        HTTPException: Als de order niet gevonden wordt of geen originele order heeft
    """
    try:
        # Haal de upsell order op
        upsell_order = crud.get_order(db, order_id)
        if not upsell_order:
            raise HTTPException(status_code=404, detail="Upsell order niet gevonden")
        
        # Controleer of dit een upsell order is met origin_song_id
        if not upsell_order.origin_song_id:
            raise HTTPException(
                status_code=400, 
                detail="Deze order heeft geen gekoppelde originele order"
            )
        
        # Haal de originele order op
        original_order = db.query(Order).filter_by(
            order_id=upsell_order.origin_song_id
        ).first()
        
        if not original_order:
            raise HTTPException(
                status_code=404, 
                detail=f"Originele order {upsell_order.origin_song_id} niet gevonden"
            )
        
        # Haal de songtekst op (kan in songtekst veld of raw_data zitten)
        original_songtext = ""
        if hasattr(original_order, 'songtekst') and original_order.songtekst:
            original_songtext = original_order.songtekst
        elif original_order.raw_data and original_order.raw_data.get('songtekst'):
            original_songtext = original_order.raw_data['songtekst']
        
        return JSONResponse(
            content={
                "success": True,
                "original_songtext": original_songtext,
                "original_order_id": original_order.order_id,
                "upsell_order_id": order_id,
                "original_order_info": {
                    "klant_naam": original_order.klant_naam,
                    "thema": original_order.thema,
                    "bestel_datum": original_order.bestel_datum.isoformat() if original_order.bestel_datum else None
                }
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fout bij ophalen originele songtekst voor order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het ophalen van de originele songtekst"
        )

@router.post("/{order_id}/update-songtext")
async def update_order_songtext(
    request: UpdateSongtextRequest,
    order_id: int = Path(..., description="Order ID"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Werkt de songtekst van een order bij.
    
    Args:
        order_id: ID van de order
        songtext: De nieuwe songtekst
        db: Database sessie
        api_key: API key voor authenticatie
        
    Returns:
        De bijgewerkte order
    """
    try:
        order = crud.get_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order niet gevonden")
        
        # Update de songtekst
        # Eerst proberen als direct attribuut
        if hasattr(order, 'songtekst'):
            order.songtekst = request.songtekst
        else:
            # Als fallback, sla op in raw_data
            if not order.raw_data:
                order.raw_data = {}
            order.raw_data['songtekst'] = request.songtekst
        
        db.commit()
        
        return JSONResponse(
            content=OrderRead.model_validate(order).model_dump(mode='json'),
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fout bij bijwerken songtekst voor order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het bijwerken van de songtekst"
        )

@router.put("/{order_id}/songtext", response_model=OrderRead)
async def update_songtext(
    order_id: int = Path(..., description="Order ID"),
    songtext_update: UpdateSongtextRequest = Body(...),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Update songtekst voor een order en synchroniseer naar gerelateerde UpSell orders.
    """
    try:
        # Haal de order op
        order = crud.get_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order niet gevonden")
        
        # Update de songtekst
        order.songtekst = songtext_update.songtekst
        
        # Commit de wijziging
        db.commit()
        db.refresh(order)
        
        # SYNCHRONISEER NAAR UPSELL ORDERS
        await sync_songtext_to_upsells(db, order_id, songtext_update.songtekst)
        
        return OrderRead.model_validate(order)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fout bij updaten songtekst voor order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het updaten van de songtekst"
        )

async def sync_songtext_to_upsells(db: Session, original_order_id: int, songtext: str):
    """
    Synchroniseer songtekst naar alle UpSell orders die gelinkt zijn aan deze originele order.
    """
    try:
        # Zoek alle UpSell orders die gelinkt zijn aan deze originele order
        upsell_orders = db.query(Order).filter(
            Order.origin_song_id == original_order_id
        ).all()
        
        if not upsell_orders:
            logger.info(f"Geen UpSell orders gevonden voor originele order {original_order_id}")
            return
        
        # Update songtekst in alle UpSell orders
        updated_count = 0
        for upsell_order in upsell_orders:
            # Alleen updaten als de UpSell order nog geen eigen songtekst heeft
            # of als de songtekst leeg is
            if not upsell_order.songtekst or upsell_order.songtekst.strip() == "":
                upsell_order.songtekst = songtext
                updated_count += 1
                logger.info(f"Songtekst gesynchroniseerd naar UpSell order {upsell_order.order_id}")
        
        if updated_count > 0:
            db.commit()
            logger.info(f"Songtekst gesynchroniseerd naar {updated_count} UpSell orders voor originele order {original_order_id}")
        else:
            logger.info(f"Geen UpSell orders bijgewerkt (alleen orders zonder bestaande songtekst)")
            
    except Exception as e:
        logger.error(f"Fout bij synchroniseren songtekst naar UpSell orders: {str(e)}")
        # Niet re-raise, want de originele update moet wel doorgaan

@router.get("/upsell-matches/{order_id}")
async def get_upsell_matches(
    order_id: int = Path(..., description="UpSell order ID"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Haalt alle mogelijke matches op voor een UpSell order met confidence scores.
    Handig voor het reviewen van dubieuze matches.
    """
    try:
        # Haal de UpSell order op
        upsell_order = crud.get_order(db, order_id)
        if not upsell_order:
            raise HTTPException(status_code=404, detail="UpSell order niet gevonden")
        
        # Check of dit een UpSell order is
        is_upsell = False
        if upsell_order.raw_data and upsell_order.raw_data.get("products"):
            for product in upsell_order.raw_data["products"]:
                pivot_type = product.get("pivot", {}).get("type")
                if pivot_type == "upsell":
                    is_upsell = True
                    break
        
        if not is_upsell:
            raise HTTPException(status_code=400, detail="Dit is geen UpSell order")
        
        # Zoek alle mogelijke matches
        from app.services.upsell_linking import calculate_linking_confidence
        from datetime import datetime, timedelta
        
        # Haal klant informatie op
        customer_email = None
        customer_name = None
        
        if upsell_order.raw_data.get("customer", {}).get("email"):
            customer_email = upsell_order.raw_data["customer"]["email"]
        elif upsell_order.raw_data.get("address", {}).get("email"):
            customer_email = upsell_order.raw_data["address"]["email"]
        
        if upsell_order.raw_data.get("address", {}).get("full_name"):
            customer_name = upsell_order.raw_data["address"]["full_name"]
        elif upsell_order.raw_data.get("customer", {}).get("name"):
            customer_name = upsell_order.raw_data["customer"]["name"]
        elif upsell_order.raw_data.get("address", {}).get("firstname"):
            firstname = upsell_order.raw_data["address"]["firstname"]
            lastname = upsell_order.raw_data["address"].get("lastname", "")
            customer_name = f"{firstname} {lastname}".strip()
        
        # Zoek originele orders
        search_start = upsell_order.bestel_datum - timedelta(days=7)
        
        potential_orders = db.query(Order).filter(
            Order.bestel_datum >= search_start,
            Order.bestel_datum < upsell_order.bestel_datum,
            Order.order_id != order_id
        ).all()
        
        matches = []
        
        for order in potential_orders:
            if order.raw_data and order.raw_data.get("products"):
                for product in order.raw_data["products"]:
                    product_id = product.get("id")
                    pivot_type = product.get("pivot", {}).get("type")
                    
                    if product_id in [274588, 289456] and pivot_type != "upsell":
                        confidence = calculate_linking_confidence(
                            upsell_order.raw_data, order, customer_email, customer_name, 
                            upsell_order.bestel_datum, db
                        )
                        
                        matches.append({
                            "order_id": order.order_id,
                            "klant_naam": order.klant_naam,
                            "klant_email": order.klant_email,
                            "voornaam": order.voornaam,
                            "bestel_datum": order.bestel_datum.isoformat() if order.bestel_datum else None,
                            "thema": order.thema,
                            "product_naam": order.product_naam,
                            "confidence": round(confidence, 1),
                            "time_diff_hours": round((upsell_order.bestel_datum - order.bestel_datum).total_seconds() / 3600, 1) if order.bestel_datum else None,
                            "is_currently_linked": order.order_id == upsell_order.origin_song_id
                        })
                        break
        
        # Sorteer op confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "upsell_order": {
                "order_id": upsell_order.order_id,
                "klant_naam": upsell_order.klant_naam,
                "klant_email": upsell_order.klant_email,
                "voornaam": upsell_order.voornaam,
                "bestel_datum": upsell_order.bestel_datum.isoformat() if upsell_order.bestel_datum else None,
                "origin_song_id": upsell_order.origin_song_id,
                "customer_email": customer_email,
                "customer_name": customer_name
            },
            "matches": matches,
            "total_matches": len(matches),
            "high_confidence_matches": len([m for m in matches if m["confidence"] > 70]),
            "ambiguous_matches": len([m for m in matches if m["confidence"] > 50 and m["confidence"] <= 70])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fout bij ophalen UpSell matches voor order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het ophalen van UpSell matches"
        )


@router.post("/upsell-matches/{order_id}/link")
async def manually_link_upsell(
    order_id: int = Path(..., description="UpSell order ID"),
    original_order_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Link een UpSell order handmatig aan een originele order.
    """
    try:
        # Haal de UpSell order op
        upsell_order = crud.get_order(db, order_id)
        if not upsell_order:
            raise HTTPException(status_code=404, detail="UpSell order niet gevonden")
        
        # Haal de originele order op
        original_order = crud.get_order(db, original_order_id)
        if not original_order:
            raise HTTPException(status_code=404, detail="Originele order niet gevonden")
        
        # Link de orders
        upsell_order.origin_song_id = original_order_id
        
        # Neem thema over als de UpSell order geen thema heeft
        if not upsell_order.thema or upsell_order.thema == '-' or upsell_order.thema == 'Onbekend':
            if original_order.thema:
                upsell_order.thema = original_order.thema
        
        db.commit()
        
        logger.info(f"UpSell order {order_id} handmatig gelinkt aan originele order {original_order_id}")
        
        return {
            "success": True,
            "message": f"UpSell order {order_id} gelinkt aan originele order {original_order_id}",
            "upsell_order_id": order_id,
            "original_order_id": original_order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fout bij handmatig linken van UpSell order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het handmatig linken"
        )
