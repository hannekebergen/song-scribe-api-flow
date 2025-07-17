"""
Pydantic schemas voor Thema API endpoints
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Base schemas
class ThemaBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Unieke thema naam (slug)")
    display_name: str = Field(..., min_length=1, max_length=100, description="Weergave naam")
    description: Optional[str] = Field(None, description="Beschrijving van het thema")
    professional_prompt: Optional[str] = Field(None, description="Professionele prompt voor dit thema")
    is_active: bool = Field(True, description="Of het thema actief is")

class ThemaElementBase(BaseModel):
    element_type: str = Field(..., min_length=1, max_length=30, description="Type element")
    content: str = Field(..., min_length=1, description="Inhoud van het element")
    usage_context: Optional[str] = Field(None, max_length=50, description="Gebruik context")
    weight: int = Field(1, ge=1, le=10, description="Gewicht voor selectie (1-10)")
    suno_format: Optional[str] = Field(None, description="Suno.ai specifieke formatting")

class ThemaRhymeSetBase(BaseModel):
    rhyme_pattern: str = Field(..., min_length=1, max_length=10, description="Rijm patroon")
    rhyme_pairs: List[List[str]] = Field(..., min_items=1, description="Lijst van rijmende paren [['woord1', 'woord2'], ...]")
    difficulty_level: str = Field("medium", description="Moeilijkheidsgraad")

# Request schemas
class ThemaCreate(ThemaBase):
    pass

class ThemaUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    professional_prompt: Optional[str] = None
    is_active: Optional[bool] = None

class ThemaElementCreate(ThemaElementBase):
    thema_id: int = Field(..., description="ID van het thema")

class ThemaElementUpdate(BaseModel):
    element_type: Optional[str] = Field(None, min_length=1, max_length=30)
    content: Optional[str] = Field(None, min_length=1)
    usage_context: Optional[str] = Field(None, max_length=50)
    weight: Optional[int] = Field(None, ge=1, le=10)
    suno_format: Optional[str] = None

class ThemaRhymeSetCreate(ThemaRhymeSetBase):
    thema_id: int = Field(..., description="ID van het thema")

class ThemaRhymeSetUpdate(BaseModel):
    rhyme_pattern: Optional[str] = Field(None, min_length=1, max_length=10)
    rhyme_pairs: Optional[List[List[str]]] = Field(None, min_items=1)
    difficulty_level: Optional[str] = None

# Response schemas
class ThemaElement(ThemaElementBase):
    id: int
    thema_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ThemaRhymeSet(ThemaRhymeSetBase):
    id: int
    thema_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Thema(ThemaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    elements: List[ThemaElement] = []
    rhyme_sets: List[ThemaRhymeSet] = []

    class Config:
        from_attributes = True

class ThemaListItem(BaseModel):
    """Simplified thema voor lijst weergave"""
    id: int
    name: str
    display_name: str
    description: Optional[str]
    is_active: bool
    element_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ThemaStats(BaseModel):
    """Statistieken voor dashboard"""
    total_themas: int
    active_themas: int
    inactive_themas: int
    total_elements: int
    recent_additions: int

# Bulk operation schemas
class BulkThemaResponse(BaseModel):
    success_count: int
    error_count: int
    errors: List[str] = []

class ThemaImportItem(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    elements: List[dict] = [] 