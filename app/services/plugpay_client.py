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
        
        # Definieer de API-endpoint met expliciete include parameters voor zowel oude als nieuwe format custom fields
        url = f"https://api.plugandpay.nl/v1/orders/{order_id}?include=custom_field_inputs,custom_fields,products.custom_field_inputs,products.custom_fields,address"
        
        # Stel de headers in met de Bearer token
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # Doe het GET-verzoek
        logger.info(f"Ophalen van details voor bestelling {order_id} met alle custom fields")
        response = requests.get(url, headers=headers)
        
        # Controleer of het verzoek succesvol was
        response.raise_for_status()
        
        # Parse de JSON-response
        order_details = response.json()
        
        # Initialiseer custom_field_inputs als lege lijst als deze niet bestaat
        if not isinstance(order_details.get("custom_field_inputs"), list):
            order_details["custom_field_inputs"] = []
            
        # Controleer of er product-level custom fields zijn en voeg ze toe aan de root-level
        if "products" in order_details and isinstance(order_details["products"], list):
            for product in order_details["products"]:
                # Controleer op product-level custom_field_inputs (oude format)
                if "custom_field_inputs" in product and isinstance(product["custom_field_inputs"], list):
                    logger.info(f"Order {order_details.get('id')}: {len(product['custom_field_inputs'])} product-level custom fields gevonden")
                    # Maak een kopie van de product-level custom fields en voeg ze toe aan de root-level
                    for field in product["custom_field_inputs"]:
                        # Voeg alleen toe als het veld nog niet bestaat op root-level
                        if not any(root_field.get("id") == field.get("id") for root_field in order_details["custom_field_inputs"]):
                            order_details["custom_field_inputs"].append(field)
                            logger.debug(f"Order {order_details.get('id')}: Product-level custom field '{field.get('label')}' toegevoegd aan root-level")
                
                # Controleer op product-level custom_fields (nieuwe format)
                if "custom_fields" in product and isinstance(product["custom_fields"], list):
                    # Initialiseer custom_fields op root-level als het niet bestaat
                    if not isinstance(order_details.get("custom_fields"), list):
                        order_details["custom_fields"] = []
                    
                    # Maak een kopie van de product-level custom fields en voeg ze toe aan de root-level
                    for field in product["custom_fields"]:
                        # Voeg alleen toe als het veld nog niet bestaat op root-level
                        if not any(root_field.get("id") == field.get("id") for root_field in order_details["custom_fields"]):
                            order_details["custom_fields"].append(field)
                            logger.debug(f"Order {order_details.get('id')}: Product-level custom field (nieuwe format) '{field.get('label')}' toegevoegd aan root-level")
        
        # Log de aantal custom fields op root-level en product-level voor debugging
        root_fields_count = len(order_details.get("custom_field_inputs", []))
        product_fields_count = sum(len(product.get("custom_field_inputs", [])) for product in order_details.get("products", []) if isinstance(product, dict))
        logger.debug(f"Order {order_details.get('id')}: {root_fields_count} root-level custom fields en {product_fields_count} product-level custom fields")
        
        # Gebruik de verbeterde get_custom_fields functie om alle custom fields te verzamelen
        # De functie zal automatisch alle fallback-strategieën proberen en beide formats ondersteunen
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
            
            # Log de gevonden custom fields voor debugging
            logger.debug(f"Order {order_id}: Gevonden custom fields: {custom_fields_dict}")
        
        # Zorg ervoor dat we ook de nieuwe format custom fields hebben in de order_details
        # Dit is voor compatibiliteit met nieuwere code die mogelijk de nieuwe format verwacht
        if custom_fields_dict and not order_details.get("custom_fields"):
            # Converteer de dictionary naar het nieuwe format (label/input)
            custom_fields_new_format = []
            for label, input_value in custom_fields_dict.items():
                custom_fields_new_format.append({"label": label, "input": input_value})
            
            # Voeg de nieuwe format toe aan de order_details
            order_details["custom_fields"] = custom_fields_new_format
            logger.debug(f"Order {order_id}: Custom fields in nieuwe format toegevoegd")
        
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
