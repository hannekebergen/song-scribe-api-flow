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
        
        # Controleer of we root-level custom fields hebben ontvangen
        has_root_custom_fields = isinstance(order_details.get("custom_field_inputs"), list) and order_details.get("custom_field_inputs")
        
        # Als er geen root-level custom_field_inputs zijn, doe altijd een retry ongeacht of 'products' aanwezig is
        if not has_root_custom_fields:
            logger.warning(f"Geen root-level custom fields voor bestelling {order_id}, probeer opnieuw met expliciete include parameters")
            # Probeer opnieuw met expliciete include parameters om alle details te krijgen
            # Gebruik products.custom_field_inputs om ook de custom fields binnen products op te halen
            url = f"https://api.plugandpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products.custom_field_inputs,address"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            order_details = response.json()
        
        # Merge alle product.custom_field_inputs in order_details['custom_field_inputs']
        # Initialiseer custom_field_inputs als lege lijst als deze niet bestaat
        if not isinstance(order_details.get("custom_field_inputs"), list):
            order_details["custom_field_inputs"] = []
            
        # Verzamel alle custom fields uit products
        if order_details.get("products"):
            for product in order_details.get("products", []):
                if isinstance(product.get("custom_field_inputs"), list) and product.get("custom_field_inputs"):
                    # Log voor debugging
                    logger.debug(f"Merging {len(product.get('custom_field_inputs'))} custom fields from product in order {order_id}")
                    # Voeg alle custom fields van het product toe aan de root-level lijst
                    order_details["custom_field_inputs"].extend(product.get("custom_field_inputs"))
        
        # Log de ontvangen velden om te bevestigen dat we alle benodigde data hebben
        has_root_custom_fields = isinstance(order_details.get("custom_field_inputs"), list) and len(order_details.get("custom_field_inputs", [])) > 0
        has_products = "products" in order_details and len(order_details.get("products", [])) > 0
        has_address = "address" in order_details and order_details.get("address") is not None
        
        # Debug logging voor beschikbare keys
        logger.debug(f"Order {order_id} detail keys: {list(order_details.keys())}")
        
        # Debug logging voor custom fields
        logger.debug(f"Order {order_id} merged custom fields count: {len(order_details.get('custom_field_inputs', []))}")
        logger.debug(f"Order {order_id} custom fields: {order_details.get('custom_field_inputs')}")
        
        # Log of er custom fields in products zitten (voor debugging)
        product_custom_fields_count = sum(
            len(p.get('custom_field_inputs', [])) if isinstance(p.get('custom_field_inputs'), list) else 0
            for p in order_details.get('products', [])
        )
        logger.debug(f"Order {order_id} product custom fields count (before merge): {product_custom_fields_count}")
        
        # Na het mergen zijn alle custom fields nu in de root-level lijst
        has_product_custom_fields = product_custom_fields_count > 0
        
        # FALLBACK: Als er na de retry nog steeds geen custom fields zijn, probeer ze op te halen via de checkout endpoint
        if not has_root_custom_fields and "checkout_id" in order_details:
            checkout_id = order_details.get("checkout_id")
            logger.info(f"Geen custom fields gevonden voor order {order_id}, probeer fallback via checkout {checkout_id}")
            
            try:
                # Doe een GET-call naar de checkout endpoint
                checkout_url = f"https://api.plugandpay.nl/v1/checkouts/{checkout_id}?include=custom_field_inputs"
                checkout_response = requests.get(checkout_url, headers=headers)
                checkout_response.raise_for_status()
                checkout_data = checkout_response.json()
                
                # Controleer of er custom fields in de checkout data zitten
                if isinstance(checkout_data.get("custom_field_inputs"), list) and checkout_data.get("custom_field_inputs"):
                    # Voeg de custom fields van de checkout toe aan de order details
                    order_details["custom_field_inputs"] = checkout_data.get("custom_field_inputs")
                    logger.info(f"In checkout-fallback custom fields gevonden voor order {order_id}")
                    has_root_custom_fields = True
                else:
                    logger.info(f"Geen custom fields in checkout fallback voor order {order_id}")
            except Exception as e:
                # Log de fout, maar laat de functie doorgaan met de bestaande order_details
                logger.warning(f"Fout bij ophalen checkout data voor order {order_id}: {str(e)}")

        
        logger.info(f"Succesvol details opgehaald voor bestelling {order_id}. "
                   f"Bevat root custom fields: {has_root_custom_fields}, "
                   f"Bevat product custom fields: {has_product_custom_fields}, "
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
                
                # Debug logging om te zien welke keys beschikbaar zijn in order_details
                logger.debug(f"Order {order_id} detail keys: {list(order_details.keys())}")

                # Controleer of custom_field_inputs aanwezig is op root-niveau of binnen products
                has_custom_fields = (
                    isinstance(order_details.get('custom_field_inputs'), list)
                    and len(order_details.get('custom_field_inputs', [])) > 0
                ) or any(
                    isinstance(p.get('custom_field_inputs'), list) and p['custom_field_inputs']
                    for p in order_details.get('products', [])
                )

                # Debug logging voor custom fields
                root_custom_fields = order_details.get('custom_field_inputs')
                product_custom_fields = None
                if order_details.get('products') and len(order_details.get('products', [])) > 0:
                    product_custom_fields = order_details['products'][0].get('custom_field_inputs')
                logger.debug(f"Order {order_id} root custom fields: {root_custom_fields}")
                logger.debug(f"Order {order_id} product custom fields: {product_custom_fields}")

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
