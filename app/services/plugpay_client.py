"""
Plug&Pay API Client

Deze module bevat functies voor het communiceren met de Plug&Pay API
om ordergegevens op te halen en te verwerken.
"""

import os
import logging
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.models.order import Order

# Laad environment variables
load_dotenv()

# Configureer logging
logger = logging.getLogger(__name__)

class PlugPayAPIError(Exception):
    """Exception voor fouten bij het aanroepen van de Plug&Pay API."""
    pass

def get_api_key():
    """
    Haalt de Plug&Pay API-key op uit de environment variables.
    
    Returns:
        str: De API-key voor Plug&Pay
        
    Raises:
        PlugPayAPIError: Als de API-key niet is geconfigureerd
    """
    api_key = os.getenv("PLUGPAY_API_KEY")
    if not api_key:
        logger.error("PLUGPAY_API_KEY environment variable is niet geconfigureerd")
        raise PlugPayAPIError("Plug&Pay API-key is niet geconfigureerd")
    return api_key

def get_recent_orders():
    """
    Haalt recente bestellingen op van de Plug&Pay API.
    
    Returns:
        dict: JSON-response van de API als Python-object
        
    Raises:
        PlugPayAPIError: Bij fouten in de API-aanroep of authenticatie
    """
    try:
        # Haal de API-key op
        api_key = get_api_key()
        
        # Definieer de API-endpoint
        url = "https://api.plugandpay.nl/v1/orders"
        
        # Stel de headers in met de Bearer token
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # Doe het GET-verzoek
        logger.info("Ophalen van recente bestellingen van Plug&Pay API")
        response = requests.get(url, headers=headers)
        
        # Controleer of het verzoek succesvol was
        response.raise_for_status()
        
        # Parse de JSON-response
        orders = response.json()
        logger.debug("Raw Plug&Pay orders response: %s", orders)
        logger.info(f"Succesvol {len(orders.get('data', []))} bestellingen opgehaald van Plug&Pay API")
        
        return orders
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Fout bij het aanroepen van de Plug&Pay API: {str(e)}")
        raise PlugPayAPIError(f"Fout bij het aanroepen van de Plug&Pay API: {str(e)}")
    except ValueError as e:
        logger.error(f"Fout bij het verwerken van de JSON-response: {str(e)}")
        raise PlugPayAPIError(f"Fout bij het verwerken van de JSON-response: {str(e)}")
    except Exception as e:
        logger.error(f"Onverwachte fout bij het ophalen van bestellingen: {str(e)}")
        raise PlugPayAPIError(f"Onverwachte fout bij het ophalen van bestellingen: {str(e)}")

def get_order_details(order_id):
    """
    Haalt details van een specifieke bestelling op van de Plug&Pay API.
    
    Args:
        order_id (str): Het ID van de bestelling
        
    Returns:
        dict: JSON-response van de API als Python-object met volledige order details
        
    Raises:
        PlugPayAPIError: Bij fouten in de API-aanroep of authenticatie
    """
    try:
        # Haal de API-key op
        api_key = get_api_key()
        
        # Definieer de API-endpoint
        url = f"https://api.plugandpay.nl/v1/orders/{order_id}"
        
        # Stel de headers in met de Bearer token
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # Doe het GET-verzoek
        logger.info(f"Ophalen van details voor bestelling {order_id}")
        response = requests.get(url, headers=headers)
        
        # Controleer of het verzoek succesvol was
        response.raise_for_status()
        
        # Parse de JSON-response
        order_details = response.json()
        
        # Controleer of we de volledige data hebben ontvangen
        if not order_details.get("custom_field_inputs") and not order_details.get("products"):
            logger.warning(f"Onvolledige data ontvangen voor bestelling {order_id}, probeer opnieuw met expliciete include parameters")
            # Probeer opnieuw met expliciete include parameters om alle details te krijgen
            url = f"https://api.plugandpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products,address"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            order_details = response.json()
        
        # Log de ontvangen velden om te bevestigen dat we alle benodigde data hebben
        has_custom_fields = "custom_field_inputs" in order_details and len(order_details.get("custom_field_inputs", [])) > 0
        has_products = "products" in order_details and len(order_details.get("products", [])) > 0
        has_address = "address" in order_details and order_details.get("address") is not None
        
        logger.info(f"Succesvol details opgehaald voor bestelling {order_id}. "
                   f"Bevat custom fields: {has_custom_fields}, "
                   f"Bevat products: {has_products}, "
                   f"Bevat address: {has_address}")
        
        return order_details
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Fout bij het ophalen van bestelling {order_id}: {str(e)}")
        raise PlugPayAPIError(f"Fout bij het ophalen van bestelling {order_id}: {str(e)}")
    except ValueError as e:
        logger.error(f"Fout bij het verwerken van de JSON-response: {str(e)}")
        raise PlugPayAPIError(f"Fout bij het verwerken van de JSON-response: {str(e)}")
    except Exception as e:
        logger.error(f"Onverwachte fout bij het ophalen van bestelling {order_id}: {str(e)}")
        raise PlugPayAPIError(f"Onverwachte fout bij het ophalen van bestelling {order_id}: {str(e)}")


def fetch_and_store_recent_orders(db_session: Session):
    """
    Haalt recente bestellingen op van de Plug&Pay API en slaat ze op in de database.
    Voor elke bestelling wordt een extra call gedaan naar de detail-endpoint om de volledige
    payload met custom fields, productdetails en adresgegevens op te halen.
    
    Args:
        db_session: SQLAlchemy database sessie
        
    Returns:
        tuple: (aantal_nieuwe_bestellingen, aantal_overgeslagen_bestellingen)
        
    Raises:
        PlugPayAPIError: Bij fouten in de API-aanroep of authenticatie
    """
    try:
        # Haal recente bestellingen op (summary list)
        orders_response = get_recent_orders()
        orders = orders_response.get("data", [])
        
        if not orders:
            logger.info("Geen bestellingen gevonden om te verwerken")
            return 0, 0
        
        logger.info(f"Verwerken van {len(orders)} bestellingen uit Plug&Pay API")
        
        # Houd bij hoeveel bestellingen zijn toegevoegd of overgeslagen
        added_count = 0
        skipped_count = 0
        updated_count = 0
        
        # Verwerk elke bestelling
        for order in orders:
            order_id = order.get("id")
            if not order_id:
                logger.warning("Bestelling zonder ID overgeslagen")
                skipped_count += 1
                continue
                
            try:
                # Haal altijd eerst de volledige gedetailleerde informatie op over de bestelling
                # Dit zorgt ervoor dat we alle custom fields, products en address informatie hebben
                order_details = get_order_details(order_id)
                
                # Controleer of we de volledige data hebben ontvangen
                has_custom_fields = "custom_field_inputs" in order_details and len(order_details.get("custom_field_inputs", [])) > 0
                has_products = "products" in order_details and len(order_details.get("products", [])) > 0
                
                if not has_custom_fields or not has_products:
                    logger.warning(f"Onvolledige data voor bestelling {order_id}: custom_fields={has_custom_fields}, products={has_products}")
                
                # Controleer of de bestelling al in de database staat
                existing_order = db_session.query(Order).filter_by(order_id=order_id).first()
                
                if existing_order:
                    # Update de bestaande bestelling met de volledige raw_data
                    existing_order.raw_data = order_details
                    db_session.commit()
                    
                    logger.info(f"Bestelling {order_id} bestaat al en is bijgewerkt met volledige raw_data")
                    updated_count += 1
                    continue
                
                # Maak een nieuw Order object aan en sla het op met de volledige order_details
                _, created = Order.create_from_plugpay_data(db_session, order_details)
                
                if created:
                    added_count += 1
                else:
                    skipped_count += 1
                    
            except Exception as e:
                logger.error(f"Fout bij verwerken van bestelling {order_id}: {str(e)}")
                skipped_count += 1
        
        # Log een samenvatting
        logger.info(f"Verwerking voltooid: {added_count} nieuwe bestellingen toegevoegd, "
                   f"{updated_count} bestellingen bijgewerkt, {skipped_count} overgeslagen")
        return added_count, skipped_count
        
    except Exception as e:
        logger.error(f"Fout bij ophalen en opslaan van bestellingen: {str(e)}")
        raise PlugPayAPIError(f"Fout bij ophalen en opslaan van bestellingen: {str(e)}")
