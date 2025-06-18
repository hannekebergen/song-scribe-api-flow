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
    raw_data: Dict[str, Any] = {}
    
    @root_validator(pre=True)
    def ensure_raw_data(cls, values):
        """Zorgt ervoor dat raw_data nooit None is."""
        if values.get("raw_data") is None:
            values["raw_data"] = {}
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
    
    @root_validator(pre=True)
    def derive_fields(cls, values):
        """Leidt velden af uit raw_data.custom_field_inputs voor oudere records."""
        # 1. raw_data kan None zijn → fallback naar {}
        raw = values.get("raw_data") or {}
        
        # 2. Maak dict van custom fields (name/label → value/input)
        cf_inputs = raw.get("custom_field_inputs", [])
        if not isinstance(cf_inputs, list):
            cf_inputs = []
            
        cfs = {}
        for cf in cf_inputs:
            name = cf.get("name") or cf.get("label")
            value = cf.get("value") or cf.get("input")
            if name and value:
                cfs[name] = value
        
        # Helper functie om fallback waarden te zoeken
        def pick(*keys):
            return next((cfs[k] for k in keys if k in cfs), None)
        
        # Vul ontbrekende velden in
        values.setdefault("thema", pick("Vertel over de gelegenheid", "Gewenste stijl", "Thema"))
        values.setdefault("toon", pick("Toon", "Sfeer"))
        values.setdefault("structuur", pick("Structuur", "Song structuur"))
        values.setdefault("beschrijving", pick("Beschrijf"))
        values.setdefault("klant_naam", raw.get("address", {}).get("full_name"))
            
        # deadline afleiden uit product-titel, blijft optioneel
        if not values.get("deadline") and raw.get("products"):
            title = raw["products"][0].get("title", "")
            if "Binnen" in title and "uur" in title:
                values["deadline"] = title.replace("Songtekst - ", "")
        
        return values

    class Config:
        """Pydantic configuratie."""
        from_attributes = True
