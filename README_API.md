# JouwSong.nl API

Backend API voor jouwsong.nl om songtekstprompts te genereren op basis van klantinput.

## Functionaliteit

Deze FastAPI backend biedt de volgende functionaliteit:

- Ontvangen en verwerken van song-orderdata (via POST)
- Genereren van passende prompts voor AI-modellen (zoals ManusAI of GPT)
- Retourneren van gegenereerde prompts als JSON-response
- API-key authenticatie voor beveiligde toegang
- Modulaire structuur voor toekomstige uitbreidingen

## Projectstructuur

```
song-scribe-api-flow/
├── app/
│   ├── auth/           # Authenticatie logica
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic modellen voor data validatie
│   └── templates/       # Prompt templates voor verschillende stijlen
├── main.py             # FastAPI applicatie entry point
├── .env                # Environment variables (API key)
└── requirements.txt    # Python dependencies
```

## Installatie

1. Maak een Python virtual environment aan:

```bash
python -m venv venv
```

2. Activeer de virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Installeer de dependencies:

```bash
pip install -r requirements.txt
```

## API Starten

Start de API met Uvicorn:

```bash
uvicorn main:app --reload
```

De API is nu beschikbaar op http://localhost:8000

## API Documentatie

FastAPI genereert automatisch API documentatie:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authenticatie

De API is beveiligd met een API-key authenticatie. Voor toegang tot de endpoints moet een geldige API-key worden meegestuurd in de request headers.

### API-key Authenticatie

Voeg de API-key toe aan de request headers:

```
X-API-Key: jouwsong2025
```

Alternatief kan ook een Bearer token worden gebruikt:

```
Authorization: Bearer jouwsong2025
```

Zonder geldige authenticatie zal de API een 401 Unauthorized response geven.

## API Endpoints

### POST /api/songs/generate-prompt

Genereert een AI-prompt op basis van de ontvangen songdata. **Vereist authenticatie.**

**Request Body:**

```json
{
  "ontvanger": "Oma Corrie",
  "van": "Kleindochter Vera",
  "beschrijving": "Ze is altijd zo lief en zorgt voor iedereen. Ze houdt van tuinieren en katten.",
  "stijl": "Verjaardag",
  "extra_wens": "Mag een beetje grappig zijn, maar vooral liefdevol"
}
```

**Response:**

```json
{
  "prompt": "🎵 Prompt voor ManusAI – verjaardagslied voor Oma Corrie, geïnspireerd door de 30 populairste Nederlandse feestnummers. Je bent een ervaren Nederlandstalige songwriter gespecialiseerd in liefdevolle, grappige verjaardagsteksten. ..."
}
```

## Beschikbare Stijlen

De API ondersteunt momenteel de volgende stijlen voor songteksten:

- verjaardag
- liefde
- afscheid
- bedankt

Andere stijlen worden ook geaccepteerd, maar zullen een algemene template gebruiken.
