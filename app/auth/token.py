"""
Token-based authenticatie voor de JouwSong.nl API.

Dit module bevat de authenticatie logica voor het beschermen van API endpoints.
Momenteel wordt een eenvoudige API-key authenticatie gebruikt, maar de structuur
is voorbereid voor toekomstige uitbreiding naar JWT of OAuth2.
"""

import os
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Laad environment variables
load_dotenv()

# API key header schema voor Swagger UI documentatie
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Haal API key uit environment variables of gebruik een default waarde
# In productie: gebruik altijd environment variables en nooit hardcoded tokens
API_KEY = os.getenv("API_KEY", "jouwsong2025")

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Valideert de API key die is meegestuurd in de request header.
    
    Args:
        api_key: De API key uit de X-API-Key header
        
    Returns:
        De API key als deze geldig is
        
    Raises:
        HTTPException: Als de API key ontbreekt of ongeldig is
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key ontbreekt",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ongeldige API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key

# Alternatieve implementatie met Bearer token
# Kan gebruikt worden als alternatief voor de API key
bearer_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def get_bearer_token(authorization: str = Security(bearer_scheme)):
    """
    Valideert een Bearer token uit de Authorization header.
    
    Args:
        authorization: De Authorization header waarde
        
    Returns:
        De token als deze geldig is
        
    Raises:
        HTTPException: Als de token ontbreekt of ongeldig is
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header ontbreekt",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ongeldige authenticatie methode",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not token or token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ongeldige token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token
