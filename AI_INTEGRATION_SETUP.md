# 🤖 AI Integration Setup Guide

## 📋 Overzicht

Je Song Scribe API Flow project is nu uitgebreid met **volledige AI integratie** voor automatische songtekst generatie! Deze guide helpt je om alles op te zetten.

## 🎯 Wat is er toegevoegd?

### **Backend (Python/FastAPI)**
- ✅ **AI Client Service** (`app/services/ai_client.py`)
  - Ondersteunt OpenAI GPT, Anthropic Claude, Google Gemini
  - Automatische fallback naar dummy responses zonder API keys
  - Async/await support voor snelle responses

- ✅ **AI API Endpoints** (`app/routers/ai.py`)
  - `POST /api/ai/generate-songtext` - Genereer songtekst van prompt
  - `POST /api/ai/generate-from-order` - Genereer direct van order data
  - `POST /api/ai/enhance-prompt` - Verbeter bestaande prompts
  - `POST /api/ai/extend-songtext` - Breid songteksten uit (upsells)
  - `GET /api/ai/providers` - Beschikbare AI providers
  - `GET /api/ai/health` - Health check

### **Frontend (React/TypeScript)**
- ✅ **AI API Service** (`src/services/aiApi.ts`)
- ✅ **Verbeterde AI Prompt Card** (`src/components/order-detail/AIPromptCard.tsx`)
  - Tab interface: Prompt ↔ Songtekst
  - AI provider selectie
  - Real-time generatie met loading states
  - Error handling en status feedback

## 🛠️ Installatie

### **1. Backend Dependencies**
```bash
# Activeer je virtual environment eerst
source venv/bin/activate  # Linux/Mac
# of
venv\Scripts\activate     # Windows

# Installeer nieuwe dependency
pip install aiohttp==3.9.1

# Of installeer alle dependencies opnieuw
pip install -r requirements.txt
```

### **2. Environment Variables**
Maak een `.env` bestand aan met:

```env
# Bestaande variabelen
DATABASE_URL=postgresql://username:password@localhost/dbname
PLUGPAY_API_KEY=your_plugpay_api_key_here
API_KEY=jouwsong2025

# Nieuwe AI API Keys (voeg tenminste één toe)
OPENAI_API_KEY=sk-your-openai-api_key_here
CLAUDE_API_KEY=your-claude-api_key_here
GEMINI_API_KEY=your-gemini-api_key_here

# Optioneel
LOG_LEVEL=INFO
PORT=8000
```

### **3. Test de Integratie**
```bash
# Test AI client zonder server
python test_ai_integration.py

# Start de server
uvicorn main:app --reload

# Test API endpoints (in nieuwe terminal)
curl -X GET "http://localhost:8000/api/ai/health" \
  -H "X-API-Key: jouwsong2025"
```

## 🔑 AI Provider Setup

### **Option 1: OpenAI (Aanbevolen voor Nederlands)**
1. Ga naar [OpenAI Platform](https://platform.openai.com)
2. Maak een API key aan
3. Voeg toe als `OPENAI_API_KEY=sk-...`
4. Model gebruikt: `gpt-4o-mini` (kosteneffectief)

### **Option 2: Anthropic Claude**
1. Ga naar [Anthropic Console](https://console.anthropic.com)
2. Maak een API key aan
3. Voeg toe als `CLAUDE_API_KEY=...`
4. Model gebruikt: `claude-3-haiku-20240307`

### **Option 3: Google Gemini**
1. Ga naar [Google AI Studio](https://aistudio.google.com)
2. Maak een API key aan
3. Voeg toe als `GEMINI_API_KEY=...`
4. Model gebruikt: `gemini-pro`

### **Geen API Keys? Geen Probleem!**
Het systeem werkt ook **zonder echte API keys**:
- Genereert dummy songteksten voor testing
- Alle functionaliteit blijft beschikbaar
- Perfect voor development en demo

## 🎵 Hoe het werkt

### **Voor Standaard Orders**
1. **Order Detail** pagina → **AI Generatie** card
2. Klik **"Genereer Prompt"** → Automatische prompt op basis van order data
3. Klik **"Genereer Songtekst"** → AI maakt Nederlandse songtekst
4. **Edit/Review** → Klik **"Gebruik Deze Songtekst"**

### **Voor Upsell Orders** 
1. Systeem detecteert automatisch upsell type
2. Haalt originele songtekst op via `origin_song_id`
3. Gebruikt **extend-songtext** endpoint voor uitbreidingen
4. Behoudt stijl en toon van originele tekst

### **Workflow**
```
Order Data → Smart Prompt → AI API → Songtekst → Review → Save
```

## 🔧 Technische Details

### **AI Client Architecture**
- **Multi-provider support**: OpenAI, Claude, Gemini
- **Automatic fallback**: Dummy responses zonder API keys
- **Error handling**: Graceful degradation
- **Async/await**: Non-blocking operations
- **Token tracking**: Cost monitoring

### **API Design**
- **RESTful endpoints** met consistente response formats
- **Pydantic validation** voor type safety
- **API key authentication** voor security
- **Comprehensive error handling**

### **Frontend Integration**
- **TypeScript interfaces** voor type safety
- **React hooks** voor state management
- **Loading states** en error boundaries
- **Provider selection** UI

## 🎨 Customization

### **Prompt Templates**
Edit `app/templates/prompt_templates.py`:
```python
TEMPLATES = {
    "verjaardag": "🎵 Prompt voor {ontvanger}...",
    "liefde": "💕 Romantisch lied voor {ontvanger}...",
    # Voeg je eigen templates toe
}
```

### **AI Settings**
Pas `app/services/ai_client.py` aan:
```python
# Model selection
"model": "gpt-4o-mini",  # Change model
"temperature": 0.7,      # Creativity level
"max_tokens": 1500,      # Response length
```

## 🚀 Deployment

### **Environment Variables op Render**
```env
OPENAI_API_KEY=sk-your-key-here
CLAUDE_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
```

### **Frontend Build**
De frontend build process is ongewijzigd - alle nieuwe functionaliteit wordt automatisch meegenomen.

## 🐛 Troubleshooting

### **"No module named 'aiohttp'"**
```bash
pip install aiohttp==3.9.1
```

### **"AI API key not found"**
- Check je `.env` bestand
- Herstart de server na het toevoegen van keys
- Test met `python test_ai_integration.py`

### **"AI generation failed"**
- Check API key validity
- Check internet connection
- Review server logs voor details

### **Frontend AI card niet zichtbaar**
- Check browser console voor errors
- Verify API endpoints zijn beschikbaar
- Test met `curl` commands

## 📊 Monitoring

### **Check AI Health**
```bash
curl -X GET "http://localhost:8000/api/ai/health" \
  -H "X-API-Key: jouwsong2025"
```

### **Available Providers**
```bash
curl -X GET "http://localhost:8000/api/ai/providers" \
  -H "X-API-Key: jouwsong2025"
```

## 🎯 Next Steps

1. **Setup AI API Keys** voor productie gebruik
2. **Test verschillende providers** voor beste resultaten
3. **Customize prompt templates** voor je specifieke behoeften
4. **Monitor token usage** voor cost optimization
5. **Collect user feedback** voor prompt improvements

## 💡 Tips

- **Start met OpenAI** - beste Nederlands support
- **Use temperature 0.7** - goede balans creativiteit/consistentie
- **Test prompts extensively** - kleine wijzigingen = grote impact
- **Monitor costs** - AI API calls kosten geld
- **Backup strategy** - dummy responses als fallback

---

🎵 **Happy songwriting with AI!** 🤖✨ 