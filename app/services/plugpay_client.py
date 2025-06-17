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

def get_custom_fields(order_data, api_headers=None):
    """
    Haalt custom fields op uit order data met een robuuste fallback-strategie.
    Probeert achtereenvolgens de volgende bronnen:
    1. order["custom_field_inputs"]
    2. Eerste product["custom_field_inputs"] (indien beschikbaar)
    3. Fallback naar GET /v1/checkouts/:checkout_id?include=custom_field_inputs
    
    Args:
        order_data (dict): De order data waaruit custom fields geëxtraheerd moeten worden
        api_headers (dict, optional): Headers voor API-calls. Als None, worden headers automatisch gegenereerd.
        
    Returns:
        dict: Een dictionary met alle custom fields, waarbij de key de naam van het veld is en de value de waarde.
              Bijvoorbeeld: {"thema": "Verjaardag", "toon": "Lief", ...}
    """
    result = {}
    source_path = None
    order_id = order_data.get("id", "onbekend")
    
    # Stap 1: Probeer root-level custom fields
    if isinstance(order_data.get("custom_field_inputs"), list) and order_data.get("custom_field_inputs"):
        logger.debug(f"Order {order_id}: Root-level custom fields gevonden")
        source_path = "root"
        # Verwerk alle custom fields in een dictionary
        for field in order_data.get("custom_field_inputs", []):
            if isinstance(field, dict) and "name" in field and "value" in field:
                result[field["name"]] = field["value"]
    
    # Stap 2: Als er geen root-level fields zijn, probeer fields uit het eerste product
    if not result and order_data.get("products") and len(order_data.get("products", [])) > 0:
        first_product = order_data.get("products")[0]
        if isinstance(first_product.get("custom_field_inputs"), list) and first_product.get("custom_field_inputs"):
            logger.debug(f"Order {order_id}: Product-level custom fields gevonden")
            source_path = "product"
            # Verwerk alle custom fields in een dictionary
            for field in first_product.get("custom_field_inputs", []):
                if isinstance(field, dict) and "name" in field and "value" in field:
                    result[field["name"]] = field["value"]
    
    # Stap 3: Als er nog steeds geen fields zijn, probeer de checkout endpoint
    if not result and "checkout_id" in order_data:
        checkout_id = order_data.get("checkout_id")
        logger.debug(f"Order {order_id}: Probeer checkout fallback met ID {checkout_id}")
        
        # Genereer headers als ze niet zijn meegegeven
        if api_headers is None:
            try:
                api_key = get_api_key()
                api_headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "application/json"
                }
            except Exception as e:
                logger.error(f"Fout bij genereren API headers: {str(e)}")
                return result  # Return lege dictionary als we geen headers kunnen maken
        
        try:
            # Doe een GET-call naar de checkout endpoint
            checkout_url = f"https://api.plugandpay.nl/v1/checkouts/{checkout_id}?include=custom_field_inputs"
            checkout_response = requests.get(checkout_url, headers=api_headers)
            checkout_response.raise_for_status()
            checkout_data = checkout_response.json()
            
            # Controleer of er custom fields in de checkout data zitten
            if isinstance(checkout_data.get("custom_field_inputs"), list) and checkout_data.get("custom_field_inputs"):
                source_path = "checkout"
                logger.info(f"Order {order_id}: In checkout-fallback custom fields gevonden")
                # Verwerk alle custom fields in een dictionary
                for field in checkout_data.get("custom_field_inputs", []):
                    if isinstance(field, dict) and "name" in field and "value" in field:
                        result[field["name"]] = field["value"]
            else:
                logger.info(f"Order {order_id}: Geen custom fields in checkout fallback")
        except requests.exceptions.HTTPError as e:
            # Specifieke afhandeling voor 422-fout
            if e.response.status_code == 422:
                logger.warning(f"Order {order_id}: 422-fout bij checkout fallback (ongeldige checkout ID of niet beschikbaar)")
            else:
                logger.warning(f"Order {order_id}: HTTP-fout {e.response.status_code} bij checkout fallback")
        except Exception as e:
            # Log de fout, maar laat de functie doorgaan
            logger.warning(f"Order {order_id}: Fout bij ophalen checkout data: {str(e)}")
    
    # Log het resultaat
    if result:
        logger.info(f"Order {order_id}: {len(result)} custom fields gevonden via {source_path} path")
        logger.debug(f"Order {order_id}: Custom fields: {result}")
    else:
        logger.warning(f"Order {order_id}: Geen custom fields gevonden via alle beschikbare paden")
    
    return result


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
        
        # Probeer eerst met de standaard response
        # Als er geen custom_field_inputs zijn, doe een retry met expliciete include parameters
        if not isinstance(order_details.get("custom_field_inputs"), list) or not order_details.get("custom_field_inputs"):
            logger.warning(f"Geen root-level custom fields voor bestelling {order_id}, probeer opnieuw met expliciete include parameters")
            # Probeer opnieuw met expliciete include parameters om alle details te krijgen
            url = f"https://api.plugandpay.nl/v1/orders/{order_id}?include=custom_field_inputs,products.custom_field_inputs,address"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            order_details = response.json()
        
        # Initialiseer custom_field_inputs als lege lijst als deze niet bestaat
        if not isinstance(order_details.get("custom_field_inputs"), list):
            order_details["custom_field_inputs"] = []
        
        # Gebruik de nieuwe get_custom_fields functie om alle custom fields te verzamelen
        # De functie zal automatisch alle fallback-strategieën proberen
        custom_fields_dict = get_custom_fields(order_details, headers)
        
        # Als er custom fields zijn gevonden via de functie, zorg ervoor dat ze ook in de 
        # order_details['custom_field_inputs'] lijst staan voor compatibiliteit met bestaande code
        if custom_fields_dict:
            # Converteer de dictionary terug naar de lijst-van-dictionaries formaat
            # die verwacht wordt in order_details['custom_field_inputs']
            custom_field_list = []
            for name, value in custom_fields_dict.items():
                custom_field_list.append({"name": name, "value": value})
            
            # Vervang de bestaande custom_field_inputs met onze nieuwe, complete lijst
            order_details["custom_field_inputs"] = custom_field_list
        
        # Log de ontvangen velden om te bevestigen dat we alle benodigde data hebben
        has_custom_fields = len(custom_fields_dict) > 0
        has_products = "products" in order_details and len(order_details.get("products", [])) > 0
        has_address = "address" in order_details and order_details.get("address") is not None
        
        # Debug logging voor beschikbare keys
        logger.debug(f"Order {order_id} detail keys: {list(order_details.keys())}")
        
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
                
                # Debug logging om te zien welke keys beschikbaar zijn in order_details
                logger.debug(f"Order {order_id} detail keys: {list(order_details.keys())}")

                # Gebruik de nieuwe get_custom_fields functie om alle custom fields te verzamelen
                custom_fields_dict = get_custom_fields(order_details)
                has_custom_fields = len(custom_fields_dict) > 0
                
                # Log de gevonden custom fields voor debugging
                logger.debug(f"Order {order_id} custom fields: {custom_fields_dict}")

                has_products = "products" in order_details and len(order_details.get("products", [])) > 0
                
                if not has_custom_fields:
                    logger.warning(f"Geen custom fields gevonden voor bestelling {order_id} via alle beschikbare paden")
                    
                if not has_products:
                    logger.warning(f"Geen products gevonden voor bestelling {order_id}")
                    
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
