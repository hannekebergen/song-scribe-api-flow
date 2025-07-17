"""
AI Router voor songtekst generatie en prompt verbetering
Integreert met verschillende AI providers (OpenAI, Claude, Gemini)
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.token import get_api_key
from app.db.session import get_db
from app.config.feature_flags import is_database_prompts_enabled, is_suno_optimization_enabled

# Setup logging first
logger = logging.getLogger(__name__)

# Try to import async AI client first, fall back to sync version
try:
    from app.services.ai_client import (
        generate_songtext_from_prompt, 
        enhance_prompt, 
        extend_songtext,
        AIProvider
    )
    USE_ASYNC = True
    logger.info("Using async AI client")
except ImportError as e:
    logger.warning(f"aiohttp not available ({e}), using sync AI client")
    from app.services.ai_client_requests import (
        generate_songtext_from_prompt_sync,
        ai_client_requests
    )
    # Create sync wrappers for async functions
    async def generate_songtext_from_prompt(*args, **kwargs):
        return generate_songtext_from_prompt_sync(*args, **kwargs)
    
    async def enhance_prompt(*args, **kwargs):
        return {"success": False, "error": "Enhance prompt not implemented for sync client"}
    
    async def extend_songtext(*args, **kwargs):
        return {"success": False, "error": "Extend songtext not implemented for sync client"}
    
    from app.services.ai_client_requests import AIProvider
    USE_ASYNC = False

from app.crud.order import get_order
from app.templates.prompt_templates import generate_prompt, generate_enhanced_prompt, generate_professional_prompt

router = APIRouter(
    prefix="/api/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models voor requests en responses
class GenerateSongtextRequest(BaseModel):
    """Request model voor songtekst generatie"""
    beschrijving: str = Field(..., description="Beschrijving voor songtekst")
    provider: Optional[str] = Field(None, description="AI provider te gebruiken")
    max_tokens: int = Field(2000, description="Maximum aantal tokens", ge=100, le=4000)
    temperature: float = Field(0.7, description="Creativiteit (0.0-1.0)", ge=0.0, le=1.0)

class ProfessionalSongtextRequest(BaseModel):
    """Request model voor professionele songtekst generatie met uitgebreide prompt"""
    beschrijving: str = Field(..., description="Beschrijving voor songtekst (gebruikt in uitgebreide prompt)")
    thema_id: Optional[int] = Field(None, description="Optionele thema ID voor thema-specifieke prompt")
    max_tokens: int = Field(2000, description="Maximum aantal tokens", ge=100, le=4000)
    temperature: float = Field(0.7, description="Creativiteit (0.0-1.0)", ge=0.0, le=1.0)

class EnhancePromptRequest(BaseModel):
    """Request model voor prompt verbetering"""
    original_prompt: str = Field(..., description="De originele prompt om te verbeteren")
    order_id: int = Field(..., description="Order ID voor context")
    provider: Optional[str] = Field(None, description="AI provider te gebruiken")

class ExtendSongtextRequest(BaseModel):
    """Request model voor songtekst uitbreiding (upsells)"""
    original_songtext: str = Field(..., description="De originele songtekst")
    extension_type: str = Field(..., description="Type uitbreiding (extra_coupletten, bridge, outro)")
    additional_info: str = Field("", description="Extra informatie voor de uitbreiding")
    provider: Optional[str] = Field(None, description="AI provider te gebruiken")

class GenerateFromOrderRequest(BaseModel):
    """Request model voor het genereren van songtekst vanuit een order"""
    order_id: int = Field(..., description="Order ID om songtekst voor te genereren")
    provider: Optional[str] = Field(None, description="AI provider te gebruiken")
    max_tokens: int = Field(2000, description="Maximum aantal tokens", ge=100, le=4000)
    temperature: float = Field(0.7, description="Creativiteit (0.0-1.0)", ge=0.0, le=1.0)
    use_suno: bool = Field(False, description="Gebruik Suno.ai geoptimaliseerde prompt formatting")

class AIResponse(BaseModel):
    """Base response model voor AI operaties"""
    success: bool = Field(..., description="Of de operatie succesvol was")
    provider: str = Field(..., description="Gebruikte AI provider")
    tokens_used: Optional[int] = Field(None, description="Aantal gebruikte tokens")
    generated_at: str = Field(..., description="Tijdstip van generatie")

class SongtextResponse(AIResponse):
    """Response model voor songtekst generatie"""
    songtext: str = Field(..., description="Gegenereerde songtekst")
    prompt_length: int = Field(..., description="Lengte van de gebruikte prompt")
    is_dummy: Optional[bool] = Field(False, description="Of dit een dummy response is")

class PromptEnhancementResponse(AIResponse):
    """Response model voor prompt verbetering"""
    enhanced_prompt: str = Field(..., description="Verbeterde prompt")
    original_prompt: str = Field(..., description="Originele prompt")

class ExtensionResponse(AIResponse):
    """Response model voor songtekst uitbreiding"""
    extended_songtext: str = Field(..., description="Uitgebreide songtekst")
    original_songtext: str = Field(..., description="Originele songtekst")
    extension_type: str = Field(..., description="Type uitbreiding")

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Altijd False voor errors")
    error: str = Field(..., description="Error beschrijving")
    provider: Optional[str] = Field(None, description="Provider waar error optrad")

def _get_ai_provider(provider_str: Optional[str]) -> Optional[AIProvider]:
    """Convert string naar AIProvider enum - alleen Gemini ondersteund"""
    if not provider_str:
        return None
    
    # Alleen Gemini ondersteund
    if provider_str.lower() == "gemini":
        return AIProvider.GEMINI
    
    # Default naar Gemini voor alle andere waarden
    return AIProvider.GEMINI

@router.post("/generate-songtext", response_model=SongtextResponse)
async def generate_songtext_endpoint(
    request: GenerateSongtextRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Genereer een songtekst op basis van een prompt
    
    Deze endpoint neemt een prompt en genereert daar een Nederlandse songtekst van
    met behulp van AI. Ondersteunt verschillende AI providers.
    """
    try:
        # Genereer basic prompt van beschrijving
        basic_prompt = f"Schrijf een Nederlandse songtekst op basis van: {request.beschrijving}"
        logger.info(f"Generating songtext with prompt length: {len(basic_prompt)}")
        
        provider = _get_ai_provider(request.provider)
        
        result = await generate_songtext_from_prompt(
            prompt=basic_prompt,
            provider=provider,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        if result["success"]:
            # Voeg prompt_length toe aan het resultaat
            result["prompt_length"] = len(basic_prompt)
            return SongtextResponse(**result)
        else:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponse(
                    error=result["error"],
                    provider=result.get("provider")
                ).dict()
            )
    
    except Exception as e:
        logger.error(f"Error in generate_songtext_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(error=str(e)).dict()
        )



@router.post("/generate-from-order", response_model=SongtextResponse)
async def generate_from_order_endpoint(
    request: GenerateFromOrderRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    """
    Genereert een songtekst op basis van een order ID.
    Gebruikt altijd de professionele prompt voor optimale resultaten.
    """
    try:
        # Haal order data op
        order = get_order(db, request.order_id)
        if not order:
            return SongtextResponse(
                success=False,
                error=f"Order {request.order_id} niet gevonden"
            )
        
        # Gebruik altijd professionele prompt met thema-specifieke elementen
        song_data = {
            "ontvanger": order.voornaam or "onbekend",
            "van": order.klant_naam or "onbekend",
            "beschrijving": order.beschrijving or "",
            "stijl": order.thema or "algemeen",
            "extra_wens": order.persoonlijk_verhaal or ""
        }
        
        prompt = generate_enhanced_prompt(
            song_data, 
            db=db, 
            use_suno=getattr(request, 'use_suno', False),
            thema_id=order.thema_id
        )
        
        result = await generate_songtext_from_prompt(
            prompt=prompt,
            provider=None, # Use default provider (Gemini)
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        if result["success"]:
            return SongtextResponse(
                success=True,
                songtext=result["songtext"],
                prompt_length=len(prompt),
                provider=result["provider"],
                generated_at=result["generated_at"],
                tokens_used=result.get("tokens_used"),
                order_id=request.order_id
            )
        else:
            return SongtextResponse(
                success=False,
                error=result.get("error", "Onbekende fout bij het genereren van songtekst")
            )
        
    except Exception as e:
        logger.error(f"Error in generate_from_order_endpoint: {str(e)}")
        return SongtextResponse(
            success=False,
            error=f"Fout bij het genereren van songtekst vanaf order: {str(e)}"
        )

@router.post("/enhance-prompt", response_model=PromptEnhancementResponse)
async def enhance_prompt_endpoint(
    request: EnhancePromptRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    """
    Verbeter een bestaande prompt op basis van order context
    
    Deze endpoint neemt een bestaande prompt en maakt deze specifieker
    en gedetailleerder op basis van de order informatie.
    """
    try:
        logger.info(f"Enhancing prompt for order: {request.order_id}")
        
        # Haal order data op voor context
        order = get_order(db, request.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order_data = {
            "klant_naam": order.klant_naam or "Onbekend",
            "voor_naam": order.voor_naam or "Onbekend",
            "thema": order.thema or "Algemeen",
            "beschrijving": order.beschrijving or "Geen beschrijving"
        }
        
        provider = _get_ai_provider(request.provider)
        
        result = await enhance_prompt(
            original_prompt=request.original_prompt,
            order_data=order_data,
            provider=provider
        )
        
        if result["success"]:
            return PromptEnhancementResponse(**result)
        else:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponse(
                    error=result["error"],
                    provider=result.get("provider")
                ).dict()
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in enhance_prompt_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(error=str(e)).dict()
        )

@router.post("/extend-songtext", response_model=ExtensionResponse)
async def extend_songtext_endpoint(
    request: ExtendSongtextRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Breid een bestaande songtekst uit (voor upsell orders)
    
    Deze endpoint neemt een bestaande songtekst en breidt deze uit
    met extra coupletten, een bridge, outro, etc.
    """
    try:
        logger.info(f"Extending songtext with type: {request.extension_type}")
        
        provider = _get_ai_provider(request.provider)
        
        result = await extend_songtext(
            original_songtext=request.original_songtext,
            extension_type=request.extension_type,
            additional_info=request.additional_info,
            provider=provider
        )
        
        if result["success"]:
            return ExtensionResponse(**result)
        else:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponse(
                    error=result["error"],
                    provider=result.get("provider")
                ).dict()
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in extend_songtext_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(error=str(e)).dict()
        )

@router.post("/generate-professional-songtext", response_model=SongtextResponse)
async def generate_professional_songtext_endpoint(
    request: ProfessionalSongtextRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Genereer een songtekst met professionele thema-specifieke prompts
    
    Deze endpoint gebruikt professionele prompts die per thema zijn gedefinieerd
    in de database. Als geen thema_id wordt opgegeven, wordt de algemene 
    professionele prompt gebruikt.
    """
    try:
        # Genereer professionele prompt
        song_data = {"beschrijving": request.beschrijving}
        
        professional_prompt = generate_enhanced_prompt(
            song_data=song_data,
            db=db,
            use_suno=False,
            thema_id=request.thema_id
        )
        
        # Call AI service
        result = await generate_songtext_from_prompt(
            prompt=professional_prompt,
            provider=_get_ai_provider("openai"),  # Default to OpenAI for professional prompts
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        if result["success"]:
            return SongtextResponse(
                success=True,
                songtext=result["songtext"],
                provider=result["provider"],
                tokens_used=result.get("tokens_used"),
                generated_at=result["generated_at"],
                prompt_length=len(professional_prompt)
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponse(
                    error=result["error"],
                    provider=result.get("provider")
                ).dict()
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_professional_songtext_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(error=str(e)).dict()
        )

@router.get("/providers")
async def get_available_providers(api_key: str = Depends(get_api_key)):
    """
    Haal beschikbare AI providers op
    
    Retourneert welke AI providers beschikbaar zijn op basis van
    geconfigureerde API keys.
    """
    from app.services.ai_client import ai_client
    
    providers = []
    
    # Alleen Gemini ondersteund
    has_key = ai_client._has_api_key(AIProvider.GEMINI)
    providers.append({
        "name": AIProvider.GEMINI.value,
        "available": has_key,
        "display_name": "Google Gemini"
    })
    
    return {
        "providers": providers,
        "default_provider": ai_client.default_provider.value
    }

@router.get("/health")
async def ai_health_check():
    """
    Health check voor AI services
    
    Controleert of de AI service beschikbaar is en welke
    providers geconfigureerd zijn.
    """
    from app.services.ai_client import ai_client
    
    return {
        "status": "healthy",
        "default_provider": ai_client.default_provider.value,
        "has_gemini_key": bool(ai_client.gemini_api_key)
    }

# Suno Music Generation Endpoints
@router.post("/generate-music", response_model=dict)
async def generate_music_endpoint(
    request: dict,
    api_key: str = Depends(get_api_key)
):
    """
    Genereer volledige muziek via Suno API met Custom Mode ondersteuning
    
    Body parameters:
    - customMode: True voor Custom Mode, False voor Non-custom Mode
    - instrumental: True voor instrumentaal, False voor met zang
    - model: Model versie (V3_5, V4, V4_5)
    - style: Muziekstijl (verplicht in Custom Mode)
    - title: Titel van het lied (verplicht in Custom Mode)
    - prompt: Songtekst (verplicht als instrumental=False in Custom Mode)
    - negativeTags: Stijlen om te vermijden (optioneel)
    - songtext: Legacy parameter (wordt gemapped naar prompt)
    """
    try:
        from app.services.suno_client import generate_music_from_songtext
        
        # Check if we're using Custom Mode
        custom_mode = request.get("customMode", False)
        instrumental = request.get("instrumental", False)
        
        # Get prompt from either 'prompt' or legacy 'songtext' parameter
        prompt = request.get("prompt") or request.get("songtext", "")
        
        # Validate required fields for Custom Mode
        if custom_mode:
            if not request.get("style"):
                raise HTTPException(
                    status_code=400,
                    detail="Style is verplicht in Custom Mode"
                )
            if not request.get("title"):
                raise HTTPException(
                    status_code=400,
                    detail="Title is verplicht in Custom Mode"
                )
            if not instrumental and not prompt:
                raise HTTPException(
                    status_code=400,
                    detail="Prompt is verplicht als instrumental=False in Custom Mode"
                )
        else:
            # Non-custom mode validation
            if not prompt:
                raise HTTPException(
                    status_code=400,
                    detail="Prompt is verplicht voor muziekgeneratie"
                )
            if len(prompt) > 400:
                raise HTTPException(
                    status_code=413,
                    detail="Prompt te lang (max 400 karakters in Non-custom Mode)"
                )
        
        # Validate length limits for Custom Mode
        if custom_mode:
            model = request.get("model", "V4_5")
            max_prompt = 5000 if model == "V4_5" else 3000
            max_style = 1000 if model == "V4_5" else 200
            
            if prompt and len(prompt) > max_prompt:
                raise HTTPException(
                    status_code=413,
                    detail=f"Prompt te lang voor {model} model (max {max_prompt} karakters)"
                )
            
            style = request.get("style", "")
            if len(style) > max_style:
                raise HTTPException(
                    status_code=413,
                    detail=f"Style te lang voor {model} model (max {max_style} karakters)"
                )
            
            title = request.get("title", "")
            if len(title) > 80:
                raise HTTPException(
                    status_code=413,
                    detail="Title te lang (max 80 karakters)"
                )
        
        logger.info(f"Generating music with Suno API - Custom Mode: {custom_mode}, Instrumental: {instrumental}, Prompt length: {len(prompt)}")
        
        # Generate music - pass all parameters to the client
        result = await generate_music_from_songtext(
            songtext=prompt,  # For backward compatibility
            title=request.get("title"),
            style=request.get("style"),
            instrumental=instrumental,
            custom_mode=custom_mode,
            model=request.get("model", "V4_5"),
            negative_tags=request.get("negativeTags"),
            callback_url=request.get("callBackUrl")  # Add callback URL support
        )
        
        if result["success"]:
            # New API returns task_id instead of direct results
            return {
                "success": True,
                "task_id": result["task_id"],
                "message": result["message"],
                "status": result["status"],
                "generated_at": result["generated_at"]
            }
        else:
            # Return error from Suno API
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_music_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Muziekgeneratie mislukt: {str(e)}"
        )

@router.post("/generate-music-from-order", response_model=dict)
async def generate_music_from_order_endpoint(
    request: dict,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    """
    Genereer muziek op basis van een order ID
    
    Body parameters:
    - order_id: ID van de order
    - style: Optionele muziekstijl override
    - instrumental: True voor instrumentaal
    """
    try:
        from app.services.suno_client import generate_music_from_songtext
        
        # Validate order_id
        if not request.get("order_id"):
            raise HTTPException(
                status_code=400,
                detail="Order ID is verplicht"
            )
        
        # Get order
        order = get_order(db, request["order_id"])
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order niet gevonden"
            )
        
        # Check if order has songtext
        if not order.beschrijving and not hasattr(order, 'songtext'):
            raise HTTPException(
                status_code=400,
                detail="Order heeft geen songtekst voor muziekgeneratie"
            )
        
        # Get songtext (try songtext field first, fallback to description)
        songtext = ""
        if hasattr(order, 'songtext') and order.songtext:
            songtext = order.songtext
        elif order.beschrijving:
            songtext = order.beschrijving
        else:
            raise HTTPException(
                status_code=400,
                detail="Geen songtekst gevonden in order"
            )
        
        # Determine style based on order theme if not provided
        style = request.get("style")
        if not style and order.thema:
            # Map themes to music styles
            theme_styles = {
                "verjaardag": "pop",
                "liefde": "acoustic",
                "huwelijk": "romantic",
                "afscheid": "ballad",
                "vaderdag": "folk",
                "anders": "pop"
            }
            style = theme_styles.get(order.thema.lower(), "pop")
        
        # Generate title from order info
        title = request.get("title")
        if not title:
            if order.klant_naam:
                title = f"Lied voor {order.klant_naam}"
            else:
                title = f"Persoonlijk Lied - Order {order.order_id}"
        
        logger.info(f"Generating music for order {order.order_id} with style: {style}")
        
        # Generate music
        result = await generate_music_from_songtext(
            songtext=songtext,
            title=title,
            style=style,
            instrumental=request.get("instrumental", False)
        )
        
        if result["success"]:
            return {
                "success": True,
                "order_id": order.order_id,
                "song_id": result["song_id"],
                "title": result["title"],
                "audio_url": result["audio_url"],
                "video_url": result["video_url"],
                "image_url": result["image_url"],
                "style": result["style"],
                "model": result["model"],
                "created_at": result["created_at"],
                "generated_at": result["generated_at"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_music_from_order_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Muziekgeneratie voor order mislukt: {str(e)}"
        )

@router.get("/suno-status/{task_id}")
async def get_suno_task_status(
    task_id: str,
    api_key: str = Depends(get_api_key)
):
    """
    Controleer status van een Suno muziek generatie taak
    """
    try:
        from app.services.suno_client import SunoClient
        
        client = SunoClient()
        result = await client.get_task_status(task_id)
        
        if result.get("success"):
            return result
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error")
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking Suno task status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Status check failed: {str(e)}"
        )

@router.get("/suno-health")
async def suno_health_check(api_key: str = Depends(get_api_key)):
    """
    Health check voor Suno API integratie
    """
    try:
        from app.services.suno_client import SunoClient
        
        client = SunoClient()
        
        return {
            "status": "healthy" if client.api_key else "no_api_key",
            "has_suno_key": bool(client.api_key),
            "base_url": client.base_url,
            "api_key_length": len(client.api_key) if client.api_key else 0
        }
    except Exception as e:
        logger.error(f"Error in suno health check: {str(e)}")
        return {
            "status": "error",
            "has_suno_key": False,
            "base_url": "unknown",
            "error": str(e)
        }