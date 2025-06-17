"""
Plug&Pay API Client

Deze module bevat functies voor het communiceren met de Plug&Pay API
om ordergegevens op te halen en te verwerken.
"""

import os
import logging
import json
import requests
from typing import Any, Dict, List, Set, Tuple, Union
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.models.order import Order

# Laad environment variables
load_dotenv()

# Configureer logging
logger = logging.getLogger(__name__)


def to_safe_json(data: Any) -> Any:
    """
    Maakt een object JSON-safe door circular references te detecteren en te vervangen,
    en niet-serialiseerbare objecten om te zetten naar strings.
    
    Args:
        data: Het object dat JSON-safe gemaakt moet worden
        
    Returns:
        Een JSON-safe versie van het object
    """
    # Houd bij welke objecten al zijn verwerkt om circular references te detecteren
    processed_objects: Set[int] = set()
    # Houd bij welke velden zijn verwijderd
    removed_fields: List[str] = []
    
    # Lijst van bekende probleemvelden die uitgesloten moeten worden
    excluded_keys = ['_sa_instance_state', 'v2_data', 'object', 'session', 
                     'internal', '_internal', 'client', '_client']
    
    def process_object(obj: Any, path: str = "") -> Any:
        # Basis types kunnen direct geretourneerd worden
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
            
        # Detecteer circular references
        obj_id = id(obj)
        if obj_id in processed_objects:
            return "CIRCULAR_REF"
            
        # Voeg het object toe aan verwerkte objecten
        processed_objects.add(obj_id)
        
        try:
            # Verwerk dictionary
            if isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    # Sla uitgesloten velden over
                    if key in excluded_keys:
                        removed_fields.append(f"{path}.{key}" if path else key)
                        continue
                    # Verwerk de waarde recursief
                    result[key] = process_object(value, f"{path}.{key}" if path else key)
                return result
                
            # Verwerk lijst
            elif isinstance(obj, list):
                return [process_object(item, f"{path}[{i}]") for i, item in enumerate(obj)]
                
            # Verwerk tuple
            elif isinstance(obj, tuple):
                return tuple(process_object(item, f"{path}[{i}]") for i, item in enumerate(obj))
                
            # Andere objecten naar string converteren
            else:
                return str(obj)
                
        finally:
            # Verwijder het object uit de set van verwerkte objecten
            # zodat het in andere paden wel verwerkt kan worden
            processed_objects.remove(obj_id)
    
    # Verwerk het object
    result = process_object(data)
    
    # Log het aantal verwijderde velden
    if removed_fields:
        logger.debug(f"Verwijderde {len(removed_fields)} velden tijdens JSON-safe maken: {', '.join(removed_fields)}")
        
    return result


def dump_safe_json(data: Any) -> str:
    """
    Converteert een object naar een JSON-string, waarbij circular references
    en niet-serialiseerbare objecten veilig worden afgehandeld.
    
    Args:
        data: Het object dat naar JSON geconverteerd moet worden
        
    Returns:
        str: Een JSON-string representatie van het object
    """
    try:
        # Maak het object eerst JSON-safe
        safe_data = to_safe_json(data)
        # Converteer naar JSON met fallback naar str voor niet-serialiseerbare waarden
        return json.dumps(safe_data, default=str)
    except Exception as e:
        logger.warning(f"Fout bij serialiseren naar JSON: {e}")
        # Fallback naar een minimale versie met alleen basis informatie
        minimal_data = {
            "id": data.get("id") if isinstance(data, dict) else None,
            "error": f"Volledige data kon niet worden geserialiseerd: {e}"
        }
        return json.dumps(minimal_data)

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
    Ondersteunt zowel v1 als v2 API-structuren.
    
    Voor v2 API probeert het achtereenvolgens de volgende bronnen:
    1. order["custom_fields"] (root-level custom fields)
    2. order["items"][].custom_fields (item-level custom fields)
    3. order["items"][].product.custom_fields (product-level custom fields)
    
    Voor v1 API probeert het achtereenvolgens de volgende bronnen:
    1. order["custom_field_inputs"] (oude format met name/value)
    2. order["custom_fields"] (nieuwe format met label/input)
    3. Product-level custom fields (zowel oude als nieuwe format)
    4. Fallback naar GET /v1/checkouts/:checkout_id?include=custom_field_inputs
    
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
    
    # Helper functie om fields te extraheren uit een array, ondersteunt beide formats
    def extract_fields_from_array(fields_array, source_name):
        extracted = {}
        if isinstance(fields_array, list) and fields_array:
            logger.debug(f"Order {order_id}: {source_name} custom fields gevonden")
            for field in fields_array:
                if isinstance(field, dict):
                    # Oude format: name/value
                    if "name" in field and "value" in field:
                        extracted[field["name"]] = field["value"]
                        logger.debug(f"Order {order_id}: Oude format field gevonden: {field['name']}")
                    # Nieuwe format: label/input
                    elif "label" in field and "input" in field:
                        extracted[field["label"]] = field["input"]
                        logger.debug(f"Order {order_id}: Nieuwe format field gevonden: {field['label']}")
        return extracted
    
    # Controleer of we met v2 API data te maken hebben
    is_v2_api = "items" in order_data and isinstance(order_data.get("items"), list)
    
    if is_v2_api:
        # V2 API verwerking
        logger.debug(f"Order {order_id}: V2 API structuur gedetecteerd")
        
        # Stap 1: Verwerk root-level custom fields in v2 API
        root_fields_v2 = extract_fields_from_array(order_data.get("custom_fields", []), "V2 Root-level")
        if root_fields_v2:
            result.update(root_fields_v2)
            source_path = "v2_root"
            logger.info(f"Order {order_id}: {len(root_fields_v2)} custom fields gevonden op root-level in v2 API")
        
        # Stap 2: Verwerk item-level custom fields in v2 API
        if "items" in order_data and isinstance(order_data.get("items"), list):
            for i, item in enumerate(order_data.get("items")):
                # Item-level custom fields
                item_fields = extract_fields_from_array(
                    item.get("custom_fields", []), 
                    f"V2 Item {i+1}"
                )
                if item_fields:
                    result.update(item_fields)
                    source_path = source_path or "v2_item"
                    logger.info(f"Order {order_id}: {len(item_fields)} custom fields gevonden in item {i+1}")
                
                # Product-level custom fields binnen items
                if "product" in item and isinstance(item.get("product"), dict):
                    product_fields = extract_fields_from_array(
                        item.get("product", {}).get("custom_fields", []), 
                        f"V2 Product in item {i+1}"
                    )
                    if product_fields:
                        result.update(product_fields)
                        source_path = source_path or "v2_product"
                        logger.info(f"Order {order_id}: {len(product_fields)} custom fields gevonden in product van item {i+1}")
    else:
        # V1 API verwerking (bestaande code)
        # Stap 1: Probeer root-level custom fields in beide formats
        # 1.1: Oude format: custom_field_inputs met name/value
        root_fields = extract_fields_from_array(order_data.get("custom_field_inputs", []), "Root-level (oude format)")
        if root_fields:
            result.update(root_fields)
            source_path = "root_old_format"
        
        # 1.2: Nieuwe format: custom_fields met label/input
        root_fields_new = extract_fields_from_array(order_data.get("custom_fields", []), "Root-level (nieuwe format)")
        if root_fields_new:
            result.update(root_fields_new)
            source_path = source_path or "root_new_format"
        
        # Stap 2: Als er nog geen of onvoldoende fields zijn, probeer alle producten
        if not result or len(result) < 3:  # Als er minder dan 3 velden zijn, zoek verder
            if order_data.get("products") and isinstance(order_data.get("products"), list):
                for i, product in enumerate(order_data.get("products")):
                    # 2.1: Oude format in product
                    product_fields = extract_fields_from_array(
                        product.get("custom_field_inputs", []), 
                        f"Product {i+1} (oude format)"
                    )
                    if product_fields:
                        result.update(product_fields)
                        source_path = source_path or "product_old_format"
                    
                    # 2.2: Nieuwe format in product
                    product_fields_new = extract_fields_from_array(
                        product.get("custom_fields", []), 
                        f"Product {i+1} (nieuwe format)"
                    )
                    if product_fields_new:
                        result.update(product_fields_new)
                        source_path = source_path or "product_new_format"
    
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
            checkout_url = f"https://api.plugandpay.nl/v1/checkouts/{checkout_id}?include=custom_field_inputs,custom_fields"
            checkout_response = requests.get(checkout_url, headers=api_headers)
            checkout_response.raise_for_status()
            checkout_data = checkout_response.json()
            
            # Controleer of er custom fields in de checkout data zitten (beide formats)
            checkout_fields = extract_fields_from_array(
                checkout_data.get("custom_field_inputs", []), 
                "Checkout (oude format)"
            )
            if checkout_fields:
                result.update(checkout_fields)
                source_path = "checkout_old_format"
                logger.info(f"Order {order_id}: In checkout-fallback custom fields gevonden (oude format)")
            
            checkout_fields_new = extract_fields_from_array(
                checkout_data.get("custom_fields", []), 
                "Checkout (nieuwe format)"
            )
            if checkout_fields_new:
                result.update(checkout_fields_new)
                source_path = source_path or "checkout_new_format"
                logger.info(f"Order {order_id}: In checkout-fallback custom fields gevonden (nieuwe format)")
                
            if not checkout_fields and not checkout_fields_new:
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
    
    # Stap 4: Probeer persoonlijk verhaal uit address.note als redmiddel
    if not result.get("Beschrijf") and order_data.get("address") and order_data.get("address", {}).get("note"):
        note = order_data.get("address", {}).get("note")
        if note and len(note.strip()) > 0:
            result["Beschrijf"] = note
            logger.info(f"Order {order_id}: Persoonlijk verhaal gevonden in address.note")
            source_path = source_path or "address_note"
    
    # Stap 5: Zoek naar velden die mogelijk beschrijvingen bevatten
    if not result.get("Beschrijf"):
        # Zoek naar velden met specifieke keywords in de naam
        description_keywords = ["opmerking", "notitie", "wens", "idee", "verhaal", "vertel", "beschrijf", "toelichting"]
        for field_name, field_value in result.items():
            if any(keyword in field_name.lower() for keyword in description_keywords):
                result["Beschrijf"] = field_value
                logger.info(f"Order {order_id}: Beschrijving gevonden in alternatief veld '{field_name}'")
                source_path = source_path or "keyword_match"
                break
    
    # Stap 6: Als er nog steeds geen beschrijving is, maar wel andere velden, maak een samengestelde beschrijving
    if not result.get("Beschrijf") and len(result) > 0:
        description_parts = []
        # Voeg relevante velden samen om een beschrijving te maken
        important_fields = ["Thema", "Gelegenheid", "Toon", "Stijl", "Gewenste toon", "Structuur", "Opbouw"]
        for field in important_fields:
            if field in result:
                description_parts.append(f"{field}: {result[field]}")
        
        # Als er andere velden zijn die niet in important_fields staan, voeg die ook toe
        for field_name, field_value in result.items():
            if field_name not in important_fields and field_name not in ["Voornaam", "Achternaam", "Van", "Datum", "Deadline", "Wanneer"]:
                description_parts.append(f"{field_name}: {field_value}")
        
        if description_parts:
            result["Beschrijf"] = "\n".join(description_parts)
            logger.info(f"Order {order_id}: Samengestelde beschrijving gemaakt uit {len(description_parts)} velden")
            source_path = source_path or "composite_description"
    
    # Log het resultaat
    if result:
        logger.info(f"Order {order_id}: {len(result)} custom fields gevonden via {source_path} path")
        logger.debug(f"Order {order_id}: Custom fields: {result}")
    else:
        logger.warning(f"Order {order_id}: Geen custom fields gevonden via alle beschikbare paden")
    
    return result


def get_order_details(order_id):
    """
    Haalt details van een specifieke bestelling op van de Plug&Pay API v2.
    
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
        
        # Definieer de API-endpoint met expliciete include parameters voor v2 API
        url = f"https://api.plugandpay.nl/v2/orders/{order_id}?include=custom_fields,items,products"
        
        # Stel de headers in volgens v2 API vereisten
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "CustomApiCall/2"
        }
        
        # Doe het GET-verzoek
        logger.info(f"Ophalen van details voor bestelling {order_id} met alle custom fields")
        response = requests.get(url, headers=headers)
        
        # Controleer of het verzoek succesvol was
        response.raise_for_status()
        
        # Parse de JSON-response
        api_response = response.json()
        
        # In v2 API zit de data in een 'data' object
        if "data" not in api_response:
            logger.error(f"Order {order_id}: Onverwachte API response structuur, geen 'data' object gevonden")
            raise PlugPayAPIError(f"Onverwachte API response structuur voor order {order_id}")
            
        # Haal de order details uit de data
        order_details = api_response["data"]
        
        # Bewaar de originele v2 structuur
        order_details["v2_data"] = api_response["data"]
        
        # Initialiseer custom_fields en custom_field_inputs als lege lijsten voor compatibiliteit
        if not isinstance(order_details.get("custom_fields"), list):
            order_details["custom_fields"] = []
        
        # Voor compatibiliteit met bestaande code
        order_details["custom_field_inputs"] = []
        
        # Verwerk root-level custom fields
        if "custom_fields" in order_details and isinstance(order_details["custom_fields"], list):
            logger.info(f"Order {order_id}: {len(order_details['custom_fields'])} root-level custom fields gevonden in v2 API")
            
        # Verwerk items en hun custom fields
        if "items" in order_details and isinstance(order_details["items"], list):
            logger.info(f"Order {order_id}: {len(order_details['items'])} items gevonden in v2 API")
            
            # Voor compatibiliteit met bestaande code, zet items ook in products
            order_details["products"] = []
            
            for item_idx, item in enumerate(order_details["items"]):
                # Voeg item toe aan products voor compatibiliteit
                if "product" in item and isinstance(item["product"], dict):
                    order_details["products"].append(item["product"])
                
                # Verwerk item-level custom fields
                if "custom_fields" in item and isinstance(item["custom_fields"], list):
                    logger.info(f"Order {order_id}: Item {item_idx} heeft {len(item['custom_fields'])} custom fields")
                    
                # Verwerk product-level custom fields in items
                if "product" in item and isinstance(item["product"], dict) and "custom_fields" in item["product"] and isinstance(item["product"]["custom_fields"], list):
                    logger.info(f"Order {order_id}: Product in item {item_idx} heeft {len(item['product']['custom_fields'])} custom fields")

        
        # Gebruik de verbeterde get_custom_fields functie om alle custom fields te verzamelen uit de v2 API structuur
        # De functie zal automatisch alle locaties in de v2 API response doorzoeken
        custom_fields_dict = get_custom_fields(order_details, headers)
        
        # Log de aantal custom fields voor debugging
        root_fields_count = len(order_details.get("custom_fields", []))
        items_count = len(order_details.get("items", []))
        products_count = len(order_details.get("products", []))
        logger.debug(f"Order {order_id}: {root_fields_count} root-level custom fields, {items_count} items en {products_count} products in v2 API")
        
        # Als er custom fields zijn gevonden via de functie, zorg ervoor dat ze ook in de 
        # order_details['custom_field_inputs'] lijst staan voor compatibiliteit met bestaande code
        if custom_fields_dict:
            # Converteer de dictionary terug naar de lijst-van-dictionaries formaat
            # die verwacht wordt in order_details['custom_field_inputs'] (oude v1 format)
            custom_field_list = []
            for name, value in custom_fields_dict.items():
                custom_field_list.append({"name": name, "value": value})
            
            # Vervang de bestaande custom_field_inputs met onze nieuwe, complete lijst
            order_details["custom_field_inputs"] = custom_field_list
            
            # Log de gevonden custom fields voor debugging
            logger.debug(f"Order {order_id}: Gevonden custom fields: {custom_fields_dict}")
        
        # Zorg ervoor dat we ook de nieuwe format custom fields hebben in de order_details
        # Dit is voor compatibiliteit met nieuwere code die mogelijk de nieuwe format verwacht
        if custom_fields_dict:
            # Converteer de dictionary naar het nieuwe format (label/input)
            custom_fields_new_format = []
            for label, input_value in custom_fields_dict.items():
                custom_fields_new_format.append({"label": label, "input": input_value})
            
            # Voeg de nieuwe format toe aan de order_details
            order_details["custom_fields"] = custom_fields_new_format
            logger.debug(f"Order {order_id}: Custom fields in nieuwe format toegevoegd")
            
        # Zorg ervoor dat address informatie beschikbaar is voor compatibiliteit
        if "address" not in order_details and "billing_address" in order_details:
            order_details["address"] = order_details["billing_address"]
            logger.debug(f"Order {order_id}: Billing address gekopieerd naar address voor compatibiliteit")
        
        # Log de ontvangen velden om te bevestigen dat we alle benodigde data hebben
        has_custom_fields = len(custom_fields_dict) > 0
        has_products = "products" in order_details and len(order_details.get("products", [])) > 0
        has_address = "address" in order_details and order_details.get("address") is not None
        
        # Debug logging voor beschikbare keys
        logger.debug(f"Order {order_id} detail keys: {list(order_details.keys())}")
        
        logger.info(f"Succesvol details opgehaald voor bestelling {order_id}. "
                   f"Bevat custom fields: {has_custom_fields} ({len(custom_fields_dict)} velden), "
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
                    try:
                        # Gebruik dump_safe_json om de order_details veilig te serialiseren
                        existing_order.raw_data = json.loads(dump_safe_json(order_details))
                        db_session.commit()
                        
                        logger.info(f"Bestelling {order_id} bestaat al en is bijgewerkt met volledige raw_data")
                        updated_count += 1
                    except Exception as e:
                        logger.warning(f"Fout bij serialiseren van order {order_id} voor raw_data: {e}")
                        existing_order.raw_data = {}
                        db_session.commit()
                        logger.info(f"Bestelling {order_id} bijgewerkt met lege raw_data vanwege serialisatiefout")
                        updated_count += 1
                    continue
                
                # Maak een nieuw Order object aan en sla het op met de volledige order_details
                # Maak de order_details eerst JSON-safe
                try:
                    # Gebruik dump_safe_json om de order_details veilig te serialiseren
                    safe_order_details = json.loads(dump_safe_json(order_details))
                    _, created = Order.create_from_plugpay_data(db_session, safe_order_details)
                except Exception as e:
                    logger.warning(f"Fout bij serialiseren van order {order_id} voor raw_data: {e}")
                    # Behoud de essentiële velden maar zet raw_data op een lege dict
                    minimal_order = {
                        "id": order_details.get("id"),
                        "customer": order_details.get("customer", {}),
                        "products": order_details.get("products", []),
                        "created_at": order_details.get("created_at")
                    }
                    _, created = Order.create_from_plugpay_data(db_session, minimal_order)
                
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
