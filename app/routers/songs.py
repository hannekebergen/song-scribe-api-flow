import logging
import os
from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.song import SongRequest, PromptResponse
from app.templates.prompt_templates import generate_prompt
from app.auth.token import get_api_key

# Configureer logging
logging.basicConfig(level=logging.INFO)

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

@router.post("/webhook")
async def plugpay_webhook(request: Request):
    """
    Webhook endpoint voor Plug&Pay bestellingen.
    Ontvangt bestelgegevens en logt deze voor verdere verwerking.
    
    Args:
        request: De FastAPI request met JSON payload van Plug&Pay
        
    Returns:
        Een bevestiging dat de webhook is ontvangen
        
    Voorbeeld van verwachte Plug&Pay JSON-payload:
    ```json
    {
      "secret": "plugpay_webhook_secret_2025",
      "order_id": "12345",
      "customer": {
        "name": "Jansen",
        "email": "jansen@example.com"
      },
      "products": [
        { "id": "song-1", "name": "Verjaardagslied" },
        { "id": "song-2", "name": "Bruiloftslied" }
      ]
    }
    ```
    
    Test met curl:
    ```bash
    curl -X POST "http://localhost:8000/api/songs/webhook" \
      -H "Content-Type: application/json" \
      -d '{"secret": "plugpay_webhook_secret_2025", "order_id": "12345", "customer": {"name": "Jansen", "email": "jansen@example.com"}, "products": [{"id": "song-1", "name": "Verjaardagslied"}, {"id": "song-2", "name": "Bruiloftslied"}]}'
    ```
    """
    try:
        # Lees de JSON-body van de request
        payload = await request.json()
        
        # Controleer de geheime sleutel voor basisbeveiliging tegen ongeautoriseerde verzoeken
        expected_secret = os.getenv("PLUGPAY_SECRET")
        if not expected_secret:
            logging.warning("PLUGPAY_SECRET environment variable is niet geconfigureerd")
            # Ga door zonder validatie als de secret niet is geconfigureerd
        else:
            # Controleer of de secret aanwezig is en overeenkomt
            if "secret" not in payload:
                logging.warning(f"Secret ontbreekt in webhook verzoek van {request.client.host if request.client else 'onbekend'}")
                raise HTTPException(
                    status_code=403,
                    detail="Ongeldige authenticatie"
                )
            
            if payload["secret"] != expected_secret:
                logging.warning(f"Ongeldig secret in webhook verzoek van {request.client.host if request.client else 'onbekend'}")
                raise HTTPException(
                    status_code=403,
                    detail="Ongeldige authenticatie"
                )
            
            logging.info("Secret OK - Webhook authenticatie succesvol")
        
        # Verwerk klantgegevens en bestelinformatie uit de payload
        try:
            # Haal klantnaam en e-mailadres op
            customer_name = payload.get("customer", {}).get("name", "Onbekend")
            customer_email = payload.get("customer", {}).get("email", "Onbekend")
            order_id = payload.get("order_id", "Onbekend")
            
            # Haal productinformatie op
            products = payload.get("products", [])
            product_summary = ", ".join([f"{p.get('name', 'Onbekend')} ({p.get('id', 'Onbekend')})" for p in products])
            
            # Log een nette samenvatting van de order
            order_summary = f"""
            Nieuwe bestelling ontvangen:
            Order ID: {order_id}
            Klant: {customer_name} ({customer_email})
            Producten: {product_summary}
            """
            logging.info(order_summary)
            
            # TODO: genereer songtekst op basis van bestelling
            
        except Exception as e:
            logging.error(f"Fout bij verwerken van ordergegevens: {str(e)}")
            # Ga door met de verwerking ondanks fouten bij het parsen
        
        # Log de volledige payload voor debugging
        logging.debug(f"Volledige Plug&Pay webhook payload: {payload}")
        
        # Hier kan in de toekomst meer logica worden toegevoegd:
        # - Bestellingen opslaan in database
        # - Notificaties versturen naar klant of beheerder
        
        # Stuur een bevestiging terug
        return {"status": "ontvangen"}
    except Exception as e:
        logging.error(f"Error bij verwerken van Plug&Pay webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Er is een fout opgetreden bij het verwerken van de webhook"
        )
