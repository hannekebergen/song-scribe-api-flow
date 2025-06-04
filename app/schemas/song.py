from pydantic import BaseModel, Field
from typing import Optional

class SongRequest(BaseModel):
    """
    Schema voor het ontvangen van song-orderdata via POST requests.
    """
    ontvanger: str = Field(..., description="Persoon voor wie het lied is bedoeld")
    van: str = Field(..., description="Persoon die het lied bestelt/geeft")
    beschrijving: str = Field(..., description="Beschrijving van de ontvanger en context")
    stijl: str = Field(..., description="Stijl van het lied (bijv. 'Verjaardag', 'Liefde')")
    extra_wens: Optional[str] = Field(None, description="Extra wensen voor het lied")

class PromptResponse(BaseModel):
    """
    Schema voor de gegenereerde prompt als respons.
    """
    prompt: str = Field(..., description="Gegenereerde prompt voor AI-model")
