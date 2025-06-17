"""
Pydantic schemas voor Order modellen.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


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

    class Config:
        """Pydantic configuratie."""
        from_attributes = True
