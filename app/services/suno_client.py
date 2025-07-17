"""
Suno AI Client Service voor muziekgeneratie
Integreert met Suno API om volledige liedjes te genereren van songteksten
"""

import os
import json
import logging
import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Import both aiohttp and requests
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    logger.warning("aiohttp not available")

# Always import requests for sync operations
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.error("requests not available - sync operations will fail")

class SunoClient:
    """
    Client voor het aanroepen van de Suno API voor muziekgeneratie
    """
    
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")
        # Updated to correct SUNO API endpoint
        self.base_url = "https://api.sunoapi.org/api/v1"
        
        if not self.api_key:
            logger.warning("SUNO_API_KEY niet gevonden - muziekgeneratie werkt niet")
        else:
            logger.info("Suno Client initialized with API key")
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers voor Suno API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def generate_music_async(
        self, 
        songtext: str, 
        title: str = None,
        style: str = None,
        instrumental: bool = False,
        custom_mode: bool = True,
        model: str = "V4_5",
        negative_tags: str = None,
        callback_url: str = None
    ) -> Dict[str, Any]:
        """
        Genereer muziek via Suno API (async versie) met nieuwe API structuur
        
        Args:
            songtext: De songtekst om muziek voor te genereren (prompt in Custom Mode)
            title: Titel van het lied
            style: Muziekstijl (pop, jazz, acoustic, etc.)
            instrumental: True voor instrumentaal, False voor met zang
            custom_mode: True voor Custom Mode, False voor Non-custom Mode
            model: Model versie (V3_5, V4, V4_5)
            negative_tags: Stijlen om te vermijden
            callback_url: URL voor callback notifications
            
        Returns:
            Dict met success/error en task ID voor status tracking
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        if not HAS_AIOHTTP:
            # Fall back to sync version
            return self.generate_music_sync(songtext, title, style, instrumental, custom_mode, model, negative_tags, callback_url)
        
        try:
            # Prepare request data according to new Suno API documentation
            data = {
                "customMode": custom_mode,
                "instrumental": instrumental,
                "model": model,
                "callBackUrl": callback_url or "https://api.example.com/callback"  # Required field
            }
            
            # Add required parameters for Custom Mode
            if custom_mode:
                if not title:
                    return {
                        "success": False,
                        "error": "Title is required for Custom Mode"
                    }
                if not style:
                    return {
                        "success": False,
                        "error": "Style is required for Custom Mode"
                    }
                
                data["title"] = title
                data["style"] = style
                
                if not instrumental and songtext:
                    data["prompt"] = songtext
            else:
                # Non-custom mode - only prompt is required
                if songtext:
                    data["prompt"] = songtext
                else:
                    return {
                        "success": False,
                        "error": "Prompt is required for Non-custom Mode"
                    }
            
            # Add optional parameters
            if negative_tags:
                data["negativeTags"] = negative_tags
            
            logger.info(f"Sending request to Suno API: {json.dumps(data, indent=2)}")
            
            # Make async request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate",
                    json=data,
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=180)  # 3 minuten timeout
                ) as response:
                    
                    response_text = await response.text()
                    logger.info(f"Suno API response: {response.status} - {response_text}")
                    
                    if response.status == 200:
                        result = json.loads(response_text)
                        
                        # New API returns task ID for status tracking
                        if result.get("code") == 200 and result.get("data", {}).get("taskId"):
                            task_id = result["data"]["taskId"]
                            
                            return {
                                "success": True,
                                "task_id": task_id,
                                "message": "Music generation started",
                                "status": "PENDING",
                                "generated_at": datetime.utcnow().isoformat()
                            }
                        else:
                            return {
                                "success": False,
                                "error": f"Suno API returned unexpected response: {result}"
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
                    
                    elif response.status == 503:
                        return {
                            "success": False,
                            "error": "SUNO service tijdelijk niet beschikbaar - probeer over 5-10 minuten opnieuw"
                        }
                    
                    else:
                        return {
                            "success": False,
                            "error": f"Suno API error {response.status}: {response_text}"
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
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Check de status van een muziek generatie taak
        
        Args:
            task_id: De task ID van de generatie taak
            
        Returns:
            Dict met status en resultaten
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        if not HAS_AIOHTTP:
            return self.get_task_status_sync(task_id)
        
        try:
            endpoint = f"{self.base_url}/generate/record-info?taskId={task_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    endpoint,
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    response_text = await response.text()
                    
                    if response.status == 200:
                        result = json.loads(response_text)
                        
                        if result.get("code") == 200:
                            data = result.get("data", {})
                            status = data.get("status")
                            
                            # Check if we have results
                            if status == "SUCCESS" and data.get("response", {}).get("sunoData"):
                                suno_data = data["response"]["sunoData"]
                                tracks = []
                                
                                for track in suno_data:
                                    tracks.append({
                                        "id": track.get("id"),
                                        "title": track.get("title"),
                                        "audio_url": track.get("audioUrl"),
                                        "stream_url": track.get("streamAudioUrl"),
                                        "image_url": track.get("imageUrl"),
                                        "duration": track.get("duration"),
                                        "model_name": track.get("modelName"),
                                        "tags": track.get("tags"),
                                        "create_time": track.get("createTime")
                                    })
                                
                                return {
                                    "success": True,
                                    "status": status,
                                    "tracks": tracks,
                                    "task_id": task_id
                                }
                            else:
                                return {
                                    "success": True,
                                    "status": status,
                                    "task_id": task_id,
                                    "message": f"Task status: {status}"
                                }
                        else:
                            return {
                                "success": False,
                                "error": f"Suno API error: {result.get('msg', 'Unknown error')}"
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"Status check failed: {response.status} - {response_text}"
                        }
        
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return {
                "success": False,
                "error": f"Status check mislukt: {str(e)}"
            }
    
    def generate_music_sync(
        self, 
        songtext: str, 
        title: str = None,
        style: str = None,
        instrumental: bool = False,
        custom_mode: bool = True,
        model: str = "V4_5",
        negative_tags: str = None,
        callback_url: str = None
    ) -> Dict[str, Any]:
        """
        Genereer muziek via Suno API (sync versie) met nieuwe API structuur
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        if not HAS_REQUESTS:
            return {
                "success": False,
                "error": "requests module niet beschikbaar"
            }
        
        try:
            # Prepare request data according to new Suno API documentation
            data = {
                "customMode": custom_mode,
                "instrumental": instrumental,
                "model": model,
                "callBackUrl": callback_url or "https://api.example.com/callback"  # Required field
            }
            
            # Add required parameters for Custom Mode
            if custom_mode:
                if not title:
                    return {
                        "success": False,
                        "error": "Title is required for Custom Mode"
                    }
                if not style:
                    return {
                        "success": False,
                        "error": "Style is required for Custom Mode"
                    }
                
                data["title"] = title
                data["style"] = style
                
                if not instrumental and songtext:
                    data["prompt"] = songtext
            else:
                # Non-custom mode - only prompt is required
                if songtext:
                    data["prompt"] = songtext
                else:
                    return {
                        "success": False,
                        "error": "Prompt is required for Non-custom Mode"
                    }
            
            # Add optional parameters
            if negative_tags:
                data["negativeTags"] = negative_tags
            
            logger.info(f"Sending request to Suno API: {json.dumps(data, indent=2)}")
            
            # Make sync request
            response = requests.post(
                f"{self.base_url}/generate",
                json=data,
                headers=self._get_headers(),
                timeout=180  # 3 minuten timeout
            )
            
            logger.info(f"Suno API response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                
                # New API returns task ID for status tracking
                if result.get("code") == 200 and result.get("data", {}).get("taskId"):
                    task_id = result["data"]["taskId"]
                    
                    return {
                        "success": True,
                        "task_id": task_id,
                        "message": "Music generation started",
                        "status": "PENDING",
                        "generated_at": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Suno API returned unexpected response: {result}"
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
            
            elif response.status_code == 503:
                return {
                    "success": False,
                    "error": "SUNO service tijdelijk niet beschikbaar - probeer over 5-10 minuten opnieuw"
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Suno API error {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            logger.error(f"Suno API error: {str(e)}")
            return {
                "success": False,
                "error": f"Muziekgeneratie mislukt: {str(e)}"
            }
    
    def get_task_status_sync(self, task_id: str) -> Dict[str, Any]:
        """
        Check de status van een muziek generatie taak (sync versie)
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Suno API key niet geconfigureerd"
            }
        
        if not HAS_REQUESTS:
            return {
                "success": False,
                "error": "requests module niet beschikbaar"
            }
        
        try:
            endpoint = f"{self.base_url}/generate/record-info?taskId={task_id}"
            
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("code") == 200:
                    data = result.get("data", {})
                    status = data.get("status")
                    
                    # Check if we have results
                    if status == "SUCCESS" and data.get("response", {}).get("sunoData"):
                        suno_data = data["response"]["sunoData"]
                        tracks = []
                        
                        for track in suno_data:
                            tracks.append({
                                "id": track.get("id"),
                                "title": track.get("title"),
                                "audio_url": track.get("audioUrl"),
                                "stream_url": track.get("streamAudioUrl"),
                                "image_url": track.get("imageUrl"),
                                "duration": track.get("duration"),
                                "model_name": track.get("modelName"),
                                "tags": track.get("tags"),
                                "create_time": track.get("createTime")
                            })
                        
                        return {
                            "success": True,
                            "status": status,
                            "tracks": tracks,
                            "task_id": task_id
                        }
                    else:
                        return {
                            "success": True,
                            "status": status,
                            "task_id": task_id,
                            "message": f"Task status: {status}"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Suno API error: {result.get('msg', 'Unknown error')}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Status check failed: {response.status_code} - {response.text}"
                }
        
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return {
                "success": False,
                "error": f"Status check mislukt: {str(e)}"
            }

# Convenience functions
async def generate_music_from_songtext(
    songtext: str,
    title: str = None,
    style: str = None,
    instrumental: bool = False,
    custom_mode: bool = True,
    model: str = "V4_5",
    negative_tags: str = None,
    callback_url: str = None
) -> Dict[str, Any]:
    """Convenience function voor async muziek generatie"""
    client = SunoClient()
    # Use sync version for now to avoid async issues
    return client.generate_music_sync(songtext, title, style, instrumental, custom_mode, model, negative_tags, callback_url)

def generate_music_from_songtext_sync(
    songtext: str,
    title: str = None,
    style: str = None,
    instrumental: bool = False,
    custom_mode: bool = True,
    model: str = "V4_5",
    negative_tags: str = None,
    callback_url: str = None
) -> Dict[str, Any]:
    """Convenience function voor sync muziek generatie"""
    client = SunoClient()
    return client.generate_music_sync(songtext, title, style, instrumental, custom_mode, model, negative_tags, callback_url) 