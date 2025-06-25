"""
AI Client Service voor het genereren van prompts en songteksten
Ondersteunt OpenAI GPT, Anthropic Claude, en andere AI providers
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging first
logger = logging.getLogger(__name__)

# Try to import aiohttp, fall back to requests if not available
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    import requests
    HAS_AIOHTTP = False
    logger.warning("aiohttp not available, using synchronous requests")

class AIProvider(Enum):
    """Ondersteunde AI providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"

class AIClient:
    """
    Client voor het aanroepen van verschillende AI providers
    """
    
    def __init__(self):
        # API Keys uit environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Default provider
        self.default_provider = self._determine_default_provider()
        
        # API Endpoints
        self.endpoints = {
            AIProvider.OPENAI: "https://api.openai.com/v1/chat/completions",
            AIProvider.CLAUDE: "https://api.anthropic.com/v1/messages",
            AIProvider.GEMINI: "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        }
        
        logger.info(f"AI Client initialized with provider: {self.default_provider}")
    
    def _determine_default_provider(self) -> AIProvider:
        """Bepaal welke AI provider te gebruiken op basis van beschikbare API keys"""
        if self.openai_api_key:
            return AIProvider.OPENAI
        elif self.claude_api_key:
            return AIProvider.CLAUDE
        elif self.gemini_api_key:
            return AIProvider.GEMINI
        else:
            logger.warning("Geen AI API keys gevonden! Gebruik dummy mode.")
            return AIProvider.OPENAI  # Fallback
    
    def _get_headers(self, provider: AIProvider) -> Dict[str, str]:
        """Get headers voor specifieke AI provider"""
        if provider == AIProvider.OPENAI:
            return {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
        elif provider == AIProvider.CLAUDE:
            return {
                "x-api-key": self.claude_api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
        elif provider == AIProvider.GEMINI:
            return {
                "Content-Type": "application/json"
            }
        else:
            return {"Content-Type": "application/json"}
    
    def _build_openai_payload(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7) -> Dict[str, Any]:
        """Build payload voor OpenAI API"""
        return {
            "model": "gpt-4o-mini",  # Kosteneffectief model
            "messages": [
                {
                    "role": "system",
                    "content": "Je bent een professionele Nederlandse songwriter die emotionele en persoonlijke liedjes schrijft. Je schrijft altijd in het Nederlands en houdt rekening met rijm, ritme en emotionele impact."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
    
    def _build_claude_payload(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7) -> Dict[str, Any]:
        """Build payload voor Claude API"""
        return {
            "model": "claude-3-haiku-20240307",  # Snelle en kosteneffectieve versie
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": "Je bent een professionele Nederlandse songwriter die emotionele en persoonlijke liedjes schrijft. Je schrijft altijd in het Nederlands en houdt rekening met rijm, ritme en emotionele impact.",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    
    def _build_gemini_payload(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Build payload voor Gemini API"""
        full_prompt = f"""Je bent een professionele Nederlandse songwriter die emotionele en persoonlijke liedjes schrijft. Je schrijft altijd in het Nederlands en houdt rekening met rijm, ritme en emotionele impact.

{prompt}"""
        
        return {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1500,
                "topP": 1,
                "topK": 40
            }
        }
    
    async def generate_songtext(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None,
        max_tokens: int = 1500,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Genereer een songtekst op basis van een prompt
        
        Args:
            prompt: De prompt voor de AI
            provider: Welke AI provider te gebruiken (default: auto)
            max_tokens: Maximum aantal tokens in response
            temperature: Creativiteit van de AI (0.0 - 1.0)
        
        Returns:
            Dict met gegenereerde songtekst en metadata
        """
        if provider is None:
            provider = self.default_provider
        
        logger.info(f"Generating songtext with {provider.value} provider")
        
        # Check of we een API key hebben
        if not self._has_api_key(provider):
            logger.warning(f"No API key for {provider.value}, using dummy response")
            return await self._generate_dummy_songtext(prompt)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Build payload gebaseerd op provider
                if provider == AIProvider.OPENAI:
                    payload = self._build_openai_payload(prompt, max_tokens, temperature)
                    url = self.endpoints[provider]
                elif provider == AIProvider.CLAUDE:
                    payload = self._build_claude_payload(prompt, max_tokens, temperature)
                    url = self.endpoints[provider]
                elif provider == AIProvider.GEMINI:
                    payload = self._build_gemini_payload(prompt, temperature)
                    url = f"{self.endpoints[provider]}?key={self.gemini_api_key}"
                else:
                    raise ValueError(f"Unsupported provider: {provider}")
                
                headers = self._get_headers(provider)
                
                # Make API call
                async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        songtext = self._extract_songtext_from_response(result, provider)
                        
                        return {
                            "success": True,
                            "songtext": songtext,
                            "provider": provider.value,
                            "tokens_used": self._extract_tokens_used(result, provider),
                            "generated_at": datetime.now().isoformat(),
                            "prompt_length": len(prompt)
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"AI API error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "error": f"AI API returned status {response.status}",
                            "provider": provider.value
                        }
        
        except asyncio.TimeoutError:
            logger.error("AI API request timed out")
            return {
                "success": False,
                "error": "Request timed out",
                "provider": provider.value
            }
        except Exception as e:
            logger.error(f"Error calling AI API: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider.value
            }
    
    def _has_api_key(self, provider: AIProvider) -> bool:
        """Check of we een API key hebben voor de gegeven provider"""
        if provider == AIProvider.OPENAI:
            return bool(self.openai_api_key)
        elif provider == AIProvider.CLAUDE:
            return bool(self.claude_api_key)
        elif provider == AIProvider.GEMINI:
            return bool(self.gemini_api_key)
        return False
    
    def _extract_songtext_from_response(self, response: Dict[str, Any], provider: AIProvider) -> str:
        """Extract de songtekst uit de API response"""
        try:
            if provider == AIProvider.OPENAI:
                return response["choices"][0]["message"]["content"].strip()
            elif provider == AIProvider.CLAUDE:
                return response["content"][0]["text"].strip()
            elif provider == AIProvider.GEMINI:
                return response["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                return "Error: Unknown provider"
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting songtext: {e}")
            return "Error: Could not extract songtext from response"
    
    def _extract_tokens_used(self, response: Dict[str, Any], provider: AIProvider) -> Optional[int]:
        """Extract het aantal gebruikte tokens uit de response"""
        try:
            if provider == AIProvider.OPENAI:
                return response.get("usage", {}).get("total_tokens")
            elif provider == AIProvider.CLAUDE:
                return response.get("usage", {}).get("output_tokens")
            elif provider == AIProvider.GEMINI:
                # Gemini geeft niet altijd token usage terug
                return None
        except Exception:
            return None
    
    async def _generate_dummy_songtext(self, prompt: str) -> Dict[str, Any]:
        """Genereer een dummy songtekst voor testing zonder API key"""
        await asyncio.sleep(1)  # Simuleer API delay
        
        dummy_songtext = f"""🎵 **Gegenereerde Songtekst** 🎵

[Vers 1]
Dit is een voorbeeld songtekst,
Gegenereerd voor jouw verhaal.
Met emotie en met ritme,
Geschreven met veel gevoel.

[Refrein] 
Voor jou geschreven, speciaal gemaakt,
Een lied dat jouw hart raakt.
Met woorden vol van liefde,
Een melodie die blijft.

[Vers 2]
Elk verhaal is uniek en waar,
Jouw verhaal verdient dit lied.
Met zorg en aandacht geschreven,
Voor dit bijzondere moment.

[Refrein]
Voor jou geschreven, speciaal gemaakt,
Een lied dat jouw hart raakt.
Met woorden vol van liefde,
Een melodie die blijft.

---
💡 **Opmerking**: Dit is een dummy songtekst gegenereerd zonder AI API.
Voeg een echte API key toe aan je environment variables voor AI-gegenereerde content.

Prompt lengte: {len(prompt)} karakters
Gegenereerd op: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return {
            "success": True,
            "songtext": dummy_songtext,
            "provider": "dummy",
            "tokens_used": None,
            "generated_at": datetime.now().isoformat(),
            "prompt_length": len(prompt),
            "is_dummy": True
        }
    
    async def generate_prompt_enhancement(
        self,
        original_prompt: str,
        order_data: Dict[str, Any],
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """
        Verbeter een bestaande prompt op basis van order data
        
        Args:
            original_prompt: De originele prompt
            order_data: Data van de order (klant info, beschrijving, etc.)
            provider: AI provider te gebruiken
        
        Returns:
            Dict met verbeterde prompt
        """
        enhancement_prompt = f"""Verbeter de volgende prompt voor het genereren van een Nederlandse songtekst:

ORIGINELE PROMPT:
{original_prompt}

ORDER INFORMATIE:
- Klant: {order_data.get('klant_naam', 'Onbekend')}
- Voor: {order_data.get('voor_naam', 'Onbekend')}
- Thema: {order_data.get('thema', 'Algemeen')}
- Beschrijving: {order_data.get('beschrijving', 'Geen beschrijving')}

TAAK:
Maak de prompt specifieker en gedetailleerder zodat het resulteert in een betere songtekst. 
Voeg concrete instructies toe over:
1. Structuur (coupletten, refrein, bridge)
2. Toon en sfeer
3. Specifieke elementen uit de beschrijving
4. Rijmschema suggesties
5. Emotionele richting

Geef alleen de verbeterde prompt terug, geen uitleg."""

        result = await self.generate_songtext(
            enhancement_prompt,
            provider=provider,
            max_tokens=800,
            temperature=0.3  # Lagere creativiteit voor consistentere prompts
        )
        
        if result["success"]:
            return {
                "success": True,
                "enhanced_prompt": result["songtext"],
                "original_prompt": original_prompt,
                "provider": result["provider"]
            }
        else:
            return {
                "success": False,
                "error": result["error"],
                "original_prompt": original_prompt
            }
    
    async def extend_songtext_for_upsell(
        self,
        original_songtext: str,
        extension_type: str,
        additional_info: str = "",
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """
        Breid een bestaande songtekst uit voor upsell orders
        
        Args:
            original_songtext: De originele songtekst
            extension_type: Type uitbreiding ("extra_coupletten", "bridge", "outro")
            additional_info: Extra informatie voor de uitbreiding
            provider: AI provider te gebruiken
        
        Returns:
            Dict met uitgebreide songtekst
        """
        extension_prompt = f"""Breid de volgende Nederlandse songtekst uit:

ORIGINELE SONGTEKST:
{original_songtext}

UITBREIDING GEWENST: {extension_type}
EXTRA INFORMATIE: {additional_info}

INSTRUCTIES:
- Behoud dezelfde stijl, toon en rijmschema als de originele tekst
- Zorg dat de uitbreiding naadloos aansluit
- Gebruik vergelijkbare woordkeuze en thema's
- Behoud de emotionele lijn van het originele lied

TAAK: Geef de VOLLEDIGE songtekst terug (origineel + uitbreiding) in dezelfde structuur."""

        result = await self.generate_songtext(
            extension_prompt,
            provider=provider,
            max_tokens=2000,  # Meer tokens voor langere teksten
            temperature=0.5   # Matige creativiteit voor consistentie
        )
        
        if result["success"]:
            return {
                "success": True,
                "extended_songtext": result["songtext"],
                "original_songtext": original_songtext,
                "extension_type": extension_type,
                "provider": result["provider"]
            }
        else:
            return {
                "success": False,
                "error": result["error"],
                "original_songtext": original_songtext
            }

# Singleton instance
ai_client = AIClient()

# Convenience functions
async def generate_songtext_from_prompt(prompt: str, **kwargs) -> Dict[str, Any]:
    """Convenience function voor het genereren van songteksten"""
    return await ai_client.generate_songtext(prompt, **kwargs)

async def enhance_prompt(original_prompt: str, order_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Convenience function voor het verbeteren van prompts"""
    return await ai_client.generate_prompt_enhancement(original_prompt, order_data, **kwargs)

async def extend_songtext(original_songtext: str, extension_type: str, additional_info: str = "", **kwargs) -> Dict[str, Any]:
    """Convenience function voor het uitbreiden van songteksten"""
    return await ai_client.extend_songtext_for_upsell(original_songtext, extension_type, additional_info, **kwargs)