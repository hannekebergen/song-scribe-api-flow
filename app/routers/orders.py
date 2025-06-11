"""
Orders Router

Deze module bevat API endpoints voor het beheren van bestellingen.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.plugpay_client import fetch_and_store_recent_orders, PlugPayAPIError
from app.auth.token import get_api_key

# Configureer logging
logger = logging.getLogger(__name__)

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
