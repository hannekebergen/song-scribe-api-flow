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
from app.templates.prompt_templates import generate_prompt, generate_enhanced_prompt

router = APIRouter(
    prefix="/api/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models voor requests en responses
class GenerateSongtextRequest(BaseModel):
    """Request model voor songtekst generatie"""
    prompt: str = Field(..., description="De prompt voor AI songtekst generatie")
    provider: Optional[str] = Field(None, description="AI provider (openai, claude, gemini)")
    max_tokens: int = Field(1500, description="Maximum aantal tokens", ge=100, le=4000)
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
    """Request model voor songtekst generatie direct van order"""
    order_id: int = Field(..., description="Order ID om songtekst voor te genereren")
    provider: Optional[str] = Field(None, description="AI provider te gebruiken")
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
    """Convert string naar AIProvider enum"""
    if not provider_str:
        return None
    
    provider_map = {
        "openai": AIProvider.OPENAI,
        "claude": AIProvider.CLAUDE,
        "gemini": AIProvider.GEMINI
    }
    
    return provider_map.get(provider_str.lower())

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
        logger.info(f"Generating songtext with prompt length: {len(request.prompt)}")
        
        provider = _get_ai_provider(request.provider)
        
        result = await generate_songtext_from_prompt(
            prompt=request.prompt,
            provider=provider,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        if result["success"]:
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
async def generate_songtext_from_order(
    request: GenerateFromOrderRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    """
    Genereer een songtekst direct van een order
    
    Deze endpoint haalt order data op, genereert een enhanced prompt via database,
    en maakt daar een songtekst van. Gebruikt thema database voor dynamische elementen.
    """
    try:
        logger.info(f"Generating songtext for order: {request.order_id}")
        
        # Haal order data op
        order = await get_order(request.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Genereer prompt op basis van order data
        song_data = {
            "ontvanger": order.voor_naam or "Onbekend",
            "van": order.klant_naam or "Onbekend", 
            "beschrijving": order.beschrijving or "Geen beschrijving beschikbaar",
            "stijl": order.thema or "algemeen",
            "extra_wens": order.persoonlijk_verhaal or ""
        }
        
        # 🎯 Feature-flagged prompt generation
        user_id = str(order.order_id)  # Use order_id as user identifier for rollout
        
        # Check if database prompts are enabled for this request
        if is_database_prompts_enabled(user_id) and order.thema_id:
            try:
                # Check if Suno.ai optimization is also enabled
                use_suno = request.use_suno and is_suno_optimization_enabled(user_id)
                
                prompt = generate_enhanced_prompt(
                    song_data=song_data,
                    db=db,
                    use_suno=use_suno,
                    thema_id=order.thema_id
                )
                logger.info(f"Generated database-enhanced prompt: {len(prompt)} chars (thema_id: {order.thema_id}, suno: {use_suno})")
            except Exception as e:
                logger.warning(f"Database prompt generation failed, falling back to static: {str(e)}")
                # Fallback to static template
                prompt = generate_prompt(song_data)
                logger.info(f"Generated fallback static prompt: {len(prompt)} chars")
        else:
            # Use legacy static template
            prompt = generate_prompt(song_data)
            logger.info(f"Generated static prompt: {len(prompt)} chars (database prompts disabled or no thema_id)")
        
        # Genereer songtekst
        provider = _get_ai_provider(request.provider)
        
        result = await generate_songtext_from_prompt(
            prompt=prompt,
            provider=provider,
            temperature=request.temperature
        )
        
        if result["success"]:
            return SongtextResponse(**result)
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
        logger.error(f"Error in generate_songtext_from_order: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(error=str(e)).dict()
        )

@router.post("/enhance-prompt", response_model=PromptEnhancementResponse)
async def enhance_prompt_endpoint(
    request: EnhancePromptRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Verbeter een bestaande prompt op basis van order context
    
    Deze endpoint neemt een bestaande prompt en maakt deze specifieker
    en gedetailleerder op basis van de order informatie.
    """
    try:
        logger.info(f"Enhancing prompt for order: {request.order_id}")
        
        # Haal order data op voor context
        order = await get_order(request.order_id)
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

@router.get("/providers")
async def get_available_providers(api_key: str = Depends(get_api_key)):
    """
    Haal beschikbare AI providers op
    
    Retourneert welke AI providers beschikbaar zijn op basis van
    geconfigureerde API keys.
    """
    from app.services.ai_client import ai_client
    
    providers = []
    
    for provider in AIProvider:
        has_key = ai_client._has_api_key(provider)
        providers.append({
            "name": provider.value,
            "available": has_key,
            "display_name": {
                "openai": "OpenAI GPT",
                "claude": "Anthropic Claude", 
                "gemini": "Google Gemini"
            }.get(provider.value, provider.value.title())
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
        "has_openai_key": bool(ai_client.openai_api_key),
        "has_claude_key": bool(ai_client.claude_api_key),
        "has_gemini_key": bool(ai_client.gemini_api_key)
    }