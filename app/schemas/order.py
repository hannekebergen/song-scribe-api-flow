"""
Pydantic schemas voor Order modellen.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, root_validator, Field


class OrderBase(BaseModel):
    """Basis schema voor Order objecten."""
    order_id: int
    klant_naam: Optional[str] = None
    klant_email: Optional[str] = None
    product_naam: Optional[str] = None
    bestel_datum: Optional[datetime] = None


class OrderRead(BaseModel):
    """Schema voor het lezen van Order objecten."""
    id: int
    order_id: int
    klant_naam: Optional[str] = None
    klant_email: Optional[str] = None
    product_naam: Optional[str] = None
    bestel_datum: Optional[datetime] = None
    raw_data: Dict[str, Any] = {}
    
    @root_validator(pre=True)
    def ensure_raw_and_dict(cls, values: Any) -> Dict[str, Any]:
        """
        - Als 'values' een SQLAlchemy-object is → converteer naar dict via getattr.
        - Zorg vervolgens dat 'raw_data' altijd een dict ({} als fallback) is.
        """
        if not isinstance(values, dict):
            # Bewaar origineel object voor raw_data extractie
            original_values = values
            # ORM → dict met alleen beschikbare attribs
            values = {field: getattr(original_values, field, None)
                      for field in cls.model_fields}
            # voeg raw_data apart toe (kan None zijn)
            values["raw_data"] = getattr(original_values, "raw_data", None)

        # raw_data null-safe
        values["raw_data"] = values.get("raw_data") or {}
        return values
    
    # Custom fields die de frontend verwacht
    songtekst: Optional[str] = None
    status: Optional[str] = None
    voornaam: Optional[str] = None
    van_naam: Optional[str] = None
    relatie: Optional[str] = None
    datum: Optional[str] = None
    thema: Optional[str] = None
    toon: Optional[str] = None
    structuur: Optional[str] = None
    rijm: Optional[str] = None
    beschrijving: Optional[str] = None

    deadline: Optional[str] = None
    typeOrder: Optional[str] = None
    
    @root_validator(pre=True)
    def derive_fields(cls, values: Any) -> Dict[str, Any]:
        """Leidt velden af uit raw_data.custom_field_inputs voor oudere records."""
        # Zorg ervoor dat values een dict is (fallback voor als eerste validator faalt)
        if not isinstance(values, dict):
            # Als het nog steeds een Order-object is, converteer het
            original_values = values
            values = {field: getattr(original_values, field, None)
                      for field in cls.model_fields}
            values["raw_data"] = getattr(original_values, "raw_data", None)
        
        # Zorg ervoor dat raw_data een dict is
        raw = values.get("raw_data") or {}
        if raw is None:
            raw = {}
        values["raw_data"] = raw
        
        # Helper functie om custom fields te verzamelen - AANGEPAST voor echte API data
        def cf_dict():
            custom_fields = {}
            
            # Eerst proberen in products (waar de echte data zit!)
            for product in raw.get("products", []):
                for field in product.get("custom_field_inputs", []):
                    if isinstance(field, dict):
                        label = field.get("label")
                        value = field.get("input")  # Echte API gebruikt "input", niet "value"
                        if label and value:
                            custom_fields[label] = value
            
            # Fallback naar root level (legacy)
            if not custom_fields:
                lst = raw.get("custom_field_inputs") or []
                for c in lst:
                    if isinstance(c, dict):
                        key = c.get("name") or c.get("label")
                        value = c.get("value") or c.get("input")
                        if key and value:
                            custom_fields[key] = value
            
            return custom_fields
        
        cfs = cf_dict()
        
        # Helper functie om fallback waarden te zoeken
        def pick(*keys):
            return next((cfs[k] for k in keys if k in cfs), None)
        
        # Helper functie om meerdere custom fields te combineren
        def combine_fields(*keys):
            """Combineert meerdere custom field waarden tot één string."""
            values_found = []
            for key in keys:
                if key in cfs and cfs[key] and cfs[key].strip():
                    values_found.append(cfs[key].strip())
            return " ".join(values_found) if values_found else None
        
        # Vul ontbrekende velden in - AANGEPAST op basis van echte API data (2025-06-25)
        # Echte veldnamen uit API: "Beschrijf", "Vertel over de gelegenheid"
        values.setdefault("thema", pick("Vertel over de gelegenheid", "Thema", "Gelegenheid", "Voor welke gelegenheid", "Voor welke gelegenheid?", "Waarvoor is dit lied?", "Gewenste stijl"))
        values.setdefault("toon", pick("Toon", "Sfeer", "Gewenste toon", "Stijl"))
        values.setdefault("structuur", pick("Structuur", "Song structuur", "Opbouw"))
        values.setdefault("beschrijving", pick("Beschrijf", "Persoonlijk verhaal", "Vertel iets over deze persoon", "Toelichting", "Vertel over de persoon", "Vertel over deze persoon", "Vertel over je wensen", "Vertel over je ideeën", "Vertel je verhaal", "Vertel meer", "Vertel"))
        
        # Detect order type based on products
        order_type = detect_order_type(raw)
        values.setdefault("typeOrder", order_type)
        
        # Verbeterde klant informatie extractie
        address = raw.get("address", {})
        
        # Verbeterde voornaam extractie
        if not values.get("voornaam"):
            # Stap 1: Probeer eerst address.firstname
            voornaam = address.get("firstname")
            
            # Stap 2: Dan custom fields - uitgebreide lijst
            if not voornaam:
                voornaam = pick(
                    "Voornaam", 
                    "Voor wie is dit lied?", 
                    "Voor wie", 
                    "Naam",
                    "Voor wie is het lied?",
                    "Wie is de ontvanger?",
                    "Naam ontvanger",
                    "Klant naam"
                )
            
            # Stap 3: Probeer customer.name als voornaam
            if not voornaam:
                customer = raw.get("customer", {})
                if customer.get("name"):
                    # Neem alleen de voornaam (eerste woord)
                    customer_name = customer.get("name").strip()
                    voornaam = customer_name.split(' ')[0] if customer_name else None
            
            # Stap 4: Probeer uit full_name de voornaam te extraheren
            if not voornaam and address.get("full_name"):
                full_name = address.get("full_name").strip()
                voornaam = full_name.split(' ')[0] if full_name else None
            
            values.setdefault("voornaam", voornaam)
        
        # Verbeterde klantnaam extractie als fallback
        if not values.get("klant_naam"):
            # Stap 1: Probeer address.full_name
            klant_naam = address.get("full_name")
            
            # Stap 2: Combineer firstname + lastname uit address
            if not klant_naam and address.get("firstname"):
                firstname = address.get("firstname")
                lastname = address.get("lastname", "")
                klant_naam = f"{firstname} {lastname}".strip()
            
            # Stap 3: Probeer customer.name uit raw_data
            if not klant_naam:
                customer = raw.get("customer", {})
                if customer.get("name"):
                    klant_naam = customer.get("name")
            
            # Stap 4: Gebruik custom fields - uitgebreide lijst
            if not klant_naam:
                voornaam = pick(
                    "Voornaam", 
                    "Voor wie is dit lied?", 
                    "Voor wie", 
                    "Naam",
                    "Voor wie is het lied?",
                    "Wie is de ontvanger?",
                    "Naam ontvanger",
                    "Klant naam"
                )
                if voornaam:
                    achternaam = pick("Achternaam", "Van", "Familienaam", "Laatste naam")
                    klant_naam = f"{voornaam} {achternaam}".strip() if achternaam else voornaam
            
            # Stap 5: Probeer naam uit beschrijving te extraheren
            if not klant_naam:
                beschrijving = pick(
                    "Beschrijf", 
                    "Persoonlijk verhaal", 
                    "Vertel over de persoon",
                    "Toelichting"
                )
                if beschrijving and len(beschrijving.strip()) > 0:
                    # Probeer een naam te vinden in de eerste zin
                    first_sentence = beschrijving.strip().split('.')[0]
                    words = first_sentence.split(' ')
                    
                    # Zoek naar patronen die lijken op een naam
                    if len(words) >= 2:
                        potential_name = ' '.join(words[:2])
                        # Check of het begint met hoofdletters (waarschijnlijk een naam)
                        import re
                        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', potential_name):
                            klant_naam = potential_name
                        elif re.match(r'^[A-Z][a-z]+', words[0]) and len(words[0]) > 2:
                            klant_naam = words[0]
            
            # Stap 6: Laatste poging - product titel
            if not klant_naam:
                products = raw.get("products", [])
                if products and len(products) > 0:
                    product_title = products[0].get("title", "")
                    if "voor " in product_title.lower():
                        import re
                        match = re.search(r'voor ([A-Z][a-z]+(?: [A-Z][a-z]+)?)', product_title)
                        if match:
                            klant_naam = match.group(1)
            
            values.setdefault("klant_naam", klant_naam)
        
        values.setdefault("achternaam", address.get("lastname"))
        
        # Datum uit created_at
        if not values.get("datum") and raw.get("created_at"):
            values["datum"] = raw.get("created_at")
        
        # Songtekst uit raw_data halen
        if not values.get("songtekst") and raw.get("songtekst"):
            values["songtekst"] = raw["songtekst"]
        
        # Fallbacks voor kritieke DB-velden
        products = raw.get("products", [])
        if values.get("product_naam") is None and products and len(products) > 0:
            first_product = products[0]
            values["product_naam"] = first_product.get("title") or first_product.get("name") or "Onbekend product"
        
        if values.get("bestel_datum") is None:
            # Probeer ISO-date uit raw_data.created_at
            iso = raw.get("created_at")
            if not iso and products and len(products) > 0:
                # Anders uit eerste product.created_at
                iso = products[0].get("created_at")
            if iso:
                values["bestel_datum"] = iso  # laat Pydantic casten
        
        # deadline afleiden uit product-titel, blijft optioneel
        if not values.get("deadline") and products and len(products) > 0:
            title = products[0].get("title", "")
            if isinstance(title, str) and "Binnen" in title and "uur" in title:
                values["deadline"] = title.replace("Songtekst - ", "")
        
        return values

    class Config:
        """Pydantic configuratie."""
        from_attributes = True

class UpdateSongtextRequest(BaseModel):
    """Schema voor het updaten van songtekst met synchronisatie naar UpSell orders."""
    songtekst: str = Field(..., description="De nieuwe songtekst")
    sync_to_upsells: bool = Field(True, description="Of de songtekst gesynchroniseerd moet worden naar UpSell orders")

def detect_order_type(raw_data: dict) -> str:
    """Detect order type based on product information."""
    products = raw_data.get("products", [])
    
    if not products:
        return "Onbekend"
    
    # Debug logging
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"Detecting order type for {len(products)} products")
    
    # Find the main product (highest priority)
    main_order_type = None
    additional_types = []
    
    for product in products:
        product_id = product.get("id")
        pivot_type = product.get("pivot", {}).get("type")
        title = product.get("title", "") or product.get("name", "")
        
        logger.debug(f"Product: id={product_id}, pivot_type={pivot_type}, title='{title}'")
        
        # Determine product type and priority
        order_type = None
        priority = 0
        
        # Main products (highest priority)
        if product_id == 274588:
            order_type = "Standaard 72u"
            priority = 100
        elif product_id == 289456:
            order_type = "Spoed 24u"
            priority = 200
        # Upsells
        elif pivot_type == "upsell":
            if product_id == 294847:
                order_type = "Revisie"
            elif product_id == 299107:
                order_type = "Soundtrack Bundel"
            elif product_id == 299088:
                order_type = "Extra Coupletten"
            else:
                order_type = "Upsell"
            priority = 50
        # Order-bumps
        elif pivot_type == "order-bump":
            if product_id == 294792:
                order_type = "Karaoke Track"
            elif product_id == 299891:
                order_type = "Engelstalig"
            else:
                order_type = "Order-bump"
            priority = 30
        # Fallback based on title analysis
        else:
            title_lower = title.lower()
            if "24" in title or "24u" in title_lower or "24 u" in title_lower or "spoed" in title_lower:
                order_type = "Spoed 24u"
                priority = 200
            elif "72" in title or "72u" in title_lower or "72 u" in title_lower or "standaard" in title_lower:
                order_type = "Standaard 72u"
                priority = 100
            else:
                # Als we geen specifieke match hebben, probeer te raden op basis van titel
                if "songtekst" in title_lower or "lied" in title_lower:
                    order_type = "Standaard 72u"  # Default voor songtekst orders
                    priority = 100
                else:
                    order_type = "Onbekend"
                    priority = 0
        
        logger.debug(f"Determined: order_type='{order_type}', priority={priority}")
        
        # Keep track of main order type (highest priority)
        if order_type and (not main_order_type or priority > main_order_type[1]):
            if main_order_type:
                additional_types.append(main_order_type[0])
            main_order_type = (order_type, priority)
        elif order_type:
            additional_types.append(order_type)
    
    # Return combined type if we have additional types
    if main_order_type:
        result = main_order_type[0]
        if additional_types:
            result = f"{result} + {', '.join(additional_types)}"
        logger.debug(f"Final order type: '{result}'")
        return result
    
    logger.debug("No order type detected, returning 'Onbekend'")
    return "Onbekend"
