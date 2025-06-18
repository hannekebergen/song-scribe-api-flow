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
    product_naam: str
    bestel_datum: datetime


class OrderRead(BaseModel):
    """Schema voor het lezen van Order objecten."""
    id: int
    order_id: int
    klant_naam: Optional[str] = None
    klant_email: Optional[str] = None
    product_naam: str
    bestel_datum: datetime
    raw_data: Optional[Dict[str, Any]] = None
    
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
    
    @root_validator(pre=True)
    def derive_fields(cls, values):
        """Leidt velden af uit raw_data.custom_field_inputs voor oudere records."""
        raw = values.get("raw_data", {})
        
        # Bouw een dictionary van custom fields op basis van name/label en value/input
        cfs = {}
        custom_field_inputs = raw.get("custom_field_inputs", [])
        if isinstance(custom_field_inputs, list):
            for cf in custom_field_inputs:
                name = cf.get("name") or cf.get("label")
                value = cf.get("value") or cf.get("input")
                if name and value:
                    cfs[name] = value
        
        # Helper functie om fallback waarden te zoeken
        def fallback(*keys):
            return next((cfs[k] for k in keys if k in cfs), None)
        
        # Vul ontbrekende velden in
        if not values.get("thema"):
            values["thema"] = fallback("Vertel over de gelegenheid", "Gewenste stijl", "Thema")
            
        if not values.get("toon"):
            values["toon"] = fallback("Toon", "Sfeer")
            
        if not values.get("structuur"):
            values["structuur"] = fallback("Structuur", "Song structuur")
            
        if not values.get("beschrijving"):
            values["beschrijving"] = fallback("Beschrijf")
            
        if not values.get("klant_naam"):
            values["klant_naam"] = raw.get("address", {}).get("full_name")
            
        if not values.get("deadline") and "products" in raw and len(raw["products"]) > 0:
            title = raw["products"][0].get("title", "")
            if "Binnen" in title and "uur" in title:
                values["deadline"] = title.replace("Songtekst - ", "")
        
        return values

    class Config:
        """Pydantic configuratie."""
        from_attributes = True
