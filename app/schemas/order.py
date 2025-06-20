"""
Pydantic schemas voor Order modellen.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, root_validator


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
    persoonlijk_verhaal: Optional[str] = None
    deadline: Optional[str] = None
    
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
        
        # Helper functie om custom fields te verzamelen
        def cf_dict():
            lst = raw.get("custom_field_inputs") or []
            return { (c.get("name") or c.get("label")): (c.get("value") or c.get("input"))
                     for c in lst if isinstance(c, dict) }
        
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
        
        # Vul ontbrekende velden in
        values.setdefault("thema", pick("Thema", "Gelegenheid", "Vertel over de gelegenheid"))
        values.setdefault("toon", pick("Toon", "Sfeer"))
        values.setdefault("structuur", pick("Structuur", "Song structuur"))
        values.setdefault("beschrijving", pick("Beschrijf"))
        
        # Klant informatie uit address
        address = raw.get("address", {})
        values.setdefault("klant_naam", address.get("full_name"))
        values.setdefault("voornaam", address.get("firstname"))
        values.setdefault("persoonlijk_verhaal", pick("Persoonlijk verhaal"))
        
        # Datum uit created_at
        if not values.get("datum") and raw.get("created_at"):
            values["datum"] = raw.get("created_at")
        
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
