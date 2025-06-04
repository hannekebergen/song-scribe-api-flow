from fastapi import APIRouter, HTTPException, Depends
from app.schemas.song import SongRequest, PromptResponse
from app.templates.prompt_templates import generate_prompt
from app.auth.token import get_api_key

router = APIRouter(
    prefix="/api/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/generate-prompt", response_model=PromptResponse)
async def generate_song_prompt(song_request: SongRequest, api_key: str = Depends(get_api_key)):
    """
    Genereert een AI-prompt voor een songtekst op basis van de ontvangen songdata.
    
    Args:
        song_request: De gevalideerde song request data
        
    Returns:
        Een PromptResponse object met de gegenereerde prompt
    """
    try:
        # Converteer het Pydantic model naar een dictionary
        song_data = song_request.model_dump()
        
        # Genereer de prompt met behulp van de template
        prompt = generate_prompt(song_data)
        
        # Retourneer de gegenereerde prompt
        return PromptResponse(prompt=prompt)
    except Exception as e:
        # Log de error (in een echte applicatie)
        print(f"Error generating prompt: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het genereren van de prompt"
        )
