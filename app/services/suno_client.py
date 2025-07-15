"""
Suno AI Client Service voor muziekgeneratie
Integreert met Suno API om volledige liedjes te genereren van songteksten
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Try to import aiohttp, fall back to requests if not available
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    import requests
    HAS_AIOHTTP = False
    logger.warning("aiohttp not available, using synchronous requests for Suno API")

class SunoClient:
    """
    Client voor het aanroepen van de Suno API voor muziekgeneratie
    """
    
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")
        self.base_url = "https://api.suno.ai/v1"
        
        if not self.api_key:
            logger.warning("SUNO_API_KEY niet gevonden - muziekgeneratie werkt niet")
        else:
            logger.info("Suno Client initialized with API key")
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers voor Suno API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_music_async(
        self, 
        songtext: str, 
        title: str = None,
        style: str = None,
        instrumental: bool = False,
        custom_mode: bool = True,
        model: str = "V4_5",
        negative_tags: str = None
    ) -> Dict[str, Any]:
        """
        Genereer muziek via Suno API (async versie) met Custom Mode ondersteuning
        
        Args:
            songtext: De songtekst om muziek voor te genereren (prompt in Custom Mode)
            title: Titel van het lied
            style: Muziekstijl (pop, jazz, acoustic, etc.)
            instrumental: True voor instrumentaal, False voor met zang
            custom_mode: True voor Custom Mode, False voor Non-custom Mode
            model: Model versie (V3_5, V4, V4_5)
            negative_tags: Stijlen om te vermijden
            
        Returns:
            Dict met success/error en gegenereerde muziek data
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        if not HAS_AIOHTTP:
            # Fall back to sync version
            return self.generate_music_sync(songtext, title, style, instrumental, custom_mode, model, negative_tags)
        
        try:
            # Prepare request data according to Suno API documentation
            data = {
                "customMode": custom_mode,
                "instrumental": instrumental,
                "model": model
            }
            
            # Add required parameters for Custom Mode
            if custom_mode:
                if title:
                    data["title"] = title
                if style:
                    data["style"] = style
                if not instrumental and songtext:
                    data["prompt"] = songtext
            else:
                # Non-custom mode - only prompt is required
                if songtext:
                    data["prompt"] = songtext
            
            # Add optional parameters
            if negative_tags:
                data["negativeTags"] = negative_tags
            
            # Make async request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate",
                    json=data,
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=180)  # 3 minuten timeout
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Suno returns array of generated songs
                        if result.get("success") and result.get("data"):
                            song_data = result["data"][0]  # Take first result
                            
                            return {
                                "success": True,
                                "song_id": song_data.get("id"),
                                "title": song_data.get("title"),
                                "audio_url": song_data.get("audio_url"),
                                "video_url": song_data.get("video_url"),
                                "image_url": song_data.get("image_url"),
                                "lyric": song_data.get("lyric"),
                                "style": song_data.get("style"),
                                "model": song_data.get("model"),
                                "created_at": song_data.get("created_at"),
                                "generated_at": datetime.utcnow().isoformat()
                            }
                        else:
                            return {
                                "success": False,
                                "error": "Suno API returned no data"
                            }
                    
                    elif response.status == 401:
                        return {
                            "success": False,
                            "error": "Ongeldige Suno API key"
                        }
                    
                    elif response.status == 429:
                        return {
                            "success": False,
                            "error": "Rate limit bereikt - probeer over 1 minuut opnieuw"
                        }
                    
                    elif response.status == 413:
                        return {
                            "success": False,
                            "error": "Songtekst te lang voor muziekgeneratie"
                        }
                    
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"Suno API error {response.status}: {error_text}"
                        }
        
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Muziekgeneratie timeout - probeer opnieuw"
            }
        
        except Exception as e:
            logger.error(f"Suno API error: {str(e)}")
            return {
                "success": False,
                "error": f"Muziekgeneratie mislukt: {str(e)}"
            }
    
    def generate_music_sync(
        self, 
        songtext: str, 
        title: str = None,
        style: str = None,
        instrumental: bool = False,
        custom_mode: bool = True,
        model: str = "V4_5",
        negative_tags: str = None
    ) -> Dict[str, Any]:
        """
        Genereer muziek via Suno API (sync versie) met Custom Mode ondersteuning
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        try:
            # Prepare request data according to Suno API documentation
            data = {
                "customMode": custom_mode,
                "instrumental": instrumental,
                "model": model
            }
            
            # Add required parameters for Custom Mode
            if custom_mode:
                if title:
                    data["title"] = title
                if style:
                    data["style"] = style
                if not instrumental and songtext:
                    data["prompt"] = songtext
            else:
                # Non-custom mode - only prompt is required
                if songtext:
                    data["prompt"] = songtext
            
            # Add optional parameters
            if negative_tags:
                data["negativeTags"] = negative_tags
            
            # Make sync request
            response = requests.post(
                f"{self.base_url}/generate",
                json=data,
                headers=self._get_headers(),
                timeout=180  # 3 minuten timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Suno returns array of generated songs
                if result.get("success") and result.get("data"):
                    song_data = result["data"][0]  # Take first result
                    
                    return {
                        "success": True,
                        "song_id": song_data.get("id"),
                        "title": song_data.get("title"),
                        "audio_url": song_data.get("audio_url"),
                        "video_url": song_data.get("video_url"),
                        "image_url": song_data.get("image_url"),
                        "lyric": song_data.get("lyric"),
                        "style": song_data.get("style"),
                        "model": song_data.get("model"),
                        "created_at": song_data.get("created_at"),
                        "generated_at": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": "Suno API returned no data"
                    }
            
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Ongeldige Suno API key"
                }
            
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit bereikt - probeer over 1 minuut opnieuw"
                }
            
            elif response.status_code == 413:
                return {
                    "success": False,
                    "error": "Songtekst te lang voor muziekgeneratie"
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Suno API error {response.status_code}: {response.text}"
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Muziekgeneratie timeout - probeer opnieuw"
            }
        
        except Exception as e:
            logger.error(f"Suno API error: {str(e)}")
            return {
                "success": False,
                "error": f"Muziekgeneratie mislukt: {str(e)}"
            }
    
    async def get_song_status(self, song_id: str) -> Dict[str, Any]:
        """
        Controleer status van een gegenereerde song
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        try:
            if HAS_AIOHTTP:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.base_url}/songs/{song_id}",
                        headers=self._get_headers(),
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        
                        if response.status == 200:
                            return await response.json()
                        else:
                            return {
                                "success": False,
                                "error": f"Failed to get song status: {response.status}"
                            }
            else:
                # Sync version
                response = requests.get(
                    f"{self.base_url}/songs/{song_id}",
                    headers=self._get_headers(),
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get song status: {response.status_code}"
                    }
        
        except Exception as e:
            logger.error(f"Suno status check error: {str(e)}")
            return {
                "success": False,
                "error": f"Status check failed: {str(e)}"
            }

# Global client instance
suno_client = SunoClient()

# Export functions for backward compatibility
async def generate_music_from_songtext(
    songtext: str,
    title: str = None,
    style: str = None,
    instrumental: bool = False,
    custom_mode: bool = True,
    model: str = "V4_5",
    negative_tags: str = None
) -> Dict[str, Any]:
    """
    Wrapper function voor muziekgeneratie met Custom Mode ondersteuning
    """
    return await suno_client.generate_music_async(
        songtext, title, style, instrumental, custom_mode, model, negative_tags
    )

def generate_music_from_songtext_sync(
    songtext: str,
    title: str = None,
    style: str = None,
    instrumental: bool = False,
    custom_mode: bool = True,
    model: str = "V4_5",
    negative_tags: str = None
) -> Dict[str, Any]:
    """
    Sync wrapper function voor muziekgeneratie met Custom Mode ondersteuning
    """
    return suno_client.generate_music_sync(
        songtext, title, style, instrumental, custom_mode, model, negative_tags
    ) 