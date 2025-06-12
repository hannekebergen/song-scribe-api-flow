"""
Pydantic schemas voor Order modellen.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    """Basis schema voor Order objecten."""
    order_id: int
    klant_naam: Optional[str] = None
    klant_email: Optional[str] = None
    product_naam: str
    bestel_datum: datetime


class OrderRead(OrderBase):
    """Schema voor het lezen van Order objecten."""
    id: int

    class Config:
        """Pydantic configuratie."""
        orm_mode = True
