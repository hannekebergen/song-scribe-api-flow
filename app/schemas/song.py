from pydantic import BaseModel, Field
from typing import Optional, List

class SongRequest(BaseModel):
    """
    Schema voor het ontvangen van song-orderdata via POST requests.
    """
    ontvanger: str = Field(..., description="Persoon voor wie het lied is bedoeld")
    van: str = Field(..., description="Persoon die het lied bestelt/geeft")
    beschrijving: str = Field(..., description="Beschrijving van de ontvanger en context")
    stijl: str = Field(..., description="Stijl van het lied (bijv. 'Verjaardag', 'Liefde')")
    extra_wens: Optional[str] = Field(None, description="Extra wensen voor het lied")

# Alias voor SongRequest om backward compatibility te behouden
class SongPromptRequest(SongRequest):
    """Alias voor SongRequest voor backward compatibility"""
    pass

class PromptResponse(BaseModel):
    """
    Schema voor de gegenereerde prompt als respons.
    """
    prompt: str = Field(..., description="Gegenereerde prompt voor AI-model")

# Alias voor PromptResponse om backward compatibility te behouden
class SongPromptResponse(PromptResponse):
    """Alias voor PromptResponse voor backward compatibility"""
    pass

# Exporteer alle modellen
__all__ = ['SongRequest', 'SongPromptRequest', 'PromptResponse', 'SongPromptResponse']
