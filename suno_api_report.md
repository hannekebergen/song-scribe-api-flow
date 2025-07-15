
# Suno API-sleutel gebruiken voor AI-muziekgeneratie

## Inleiding
Suno is een AI-gedreven muziekplatform waarmee je vanuit korte tekstprompts complete liedjes kunt genereren – inclusief **songtekst, zang en begeleiding**. Met een Suno API-sleutel kun je deze functionaliteit integreren in je eigen applicatie of dashboard, zodat je programmatisch liedjes kunt laten maken. Dit rapport geeft een deep-dive in de Suno API: van het verkrijgen en gebruiken van de API key tot het genereren van muziek en het benutten van alle beschikbare functies. We behandelen ook voorbeeldcode (Python en JavaScript) en gaan in op foutafhandeling en rate-limiting voor een robuuste implementatie.

## API-sleutel verkrijgen en authenticatie
Om de Suno API te gebruiken heb je eerst een **API key** nodig. Registreer een account op Suno (mogelijk is een betaald abonnement vereist voor API-toegang) en navigeer naar je account/dashboard om een API-sleutel aan te maken.

**Authenticatie:** Alle API-aanvragen moeten de API-sleutel als Bearer Token in de HTTP-header meesturen:

```http
Authorization: Bearer <JOUW_API_KEY>
```

Zorg dat je deze sleutel geheim houdt en niet client-side blootstelt. Gebruik bij voorkeur environment variables of een backend‑proxy om de sleutel veilig te bewaren.

## Een lied genereren via de API
Met de Suno API kun je **volledige songs genereren** door een HTTP POST‑verzoek te sturen naar het juiste eindpunt. In de aanvraag kun je kiezen om Suno zelf lyrics te laten schrijven op basis van een prompt, of je kunt eigen lyrics aanleveren:

- **Generatie met prompt (AI‑lyrics):** Je geeft een korte omschrijving of thema voor het lied in een veld `prompt`. De AI genereert dan zelf de songtekst en muziek op basis van die prompt (*non‑custom mode*).
- **Generatie met eigen lyrics (custom mode):** Je kunt ook een volledige songtekst zelf aanleveren via een veld `lyric`. De AI componeert daar muziek (melodie, begeleiding en zang) omheen (*custom mode*).

### Belangrijke parameters
| Parameter         | Type     | Beschrijving                                                                                 |
|-------------------|----------|----------------------------------------------------------------------------------------------|
| `prompt`          | string   | Tekstprompt voor thema/genre. Vereist in non‑custom mode.                                    |
| `lyric`           | string   | Eigen songtekst voor custom mode.                                                            |
| `custom`          | boolean  | `true` bij gebruik eigen lyrics, anders `false`.                                             |
| `title`           | string   | Optioneel: liedtitel.                                                                        |
| `style`           | string   | Optioneel: stijl/genre (bijv. `"jazz"`).                                                     |
| `instrumental`    | boolean  | `true` voor instrumentaal; standaard `false`.                                                |

### Voorbeeld (Python)
```python
import requests, os

API_URL = "https://api.suno.ai/v1/generate"
API_KEY = os.getenv("SUNO_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "prompt": "Een swingend jazznummer over programmeren",
    "custom": False,
    "instrumental": False
}

r = requests.post(API_URL, json=data, headers=headers, timeout=120)
r.raise_for_status()
print(r.json())
```

### Voorbeeld (JavaScript – Fetch)
```js
const generateSong = async () => {
  const res = await fetch("https://api.suno.ai/v1/generate", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.SUNO_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      prompt: "Een swingend jazznummer over programmeren",
      custom: false,
      instrumental: false
    })
  });
  if (!res.ok) throw new Error(await res.text());
  console.log(await res.json());
};
```

### Response‑structuur (voorbeeld)
```json
{
  "success": true,
  "data": [
    {
      "id": "2f16f7bc‑4135‑42c6‑b3c5‑6d6c49dc8cd5",
      "title": "Winter Wonderland",
      "image_url": "https://cdn1.suno.ai/image_...",
      "lyric": "[Verse]\\nSnowflakes falling...",
      "audio_url": "https://cdn1.suno.ai/....mp3",
      "video_url": "https://cdn1.suno.ai/....mp4",
      "created_at": "2025‑05‑10T16:21:37Z",
      "model": "chirp‑v4",
      "prompt": "A song for Christmas",
      "style": "holiday"
    }
  ]
}
```

## Overige functies
1. **Lyrics genereren zonder audio** – ontvang alleen songtekst.  
2. **Track verlengen** – bestaande song langer maken.  
3. **Cover/Style transfer** – upload audio en genereer in nieuwe stijl.  
4. **Vocal removal** – splits zang en instrumentaal.  
5. **WAV‑conversie** – lossless export.  
6. **Muziekvideo** – eenvoudige MP4‑video met visuals.  
7. **Account/credit‑endpoint** – restant credits opvragen.

## Foutafhandeling
| Status | Betekenis                      | Aanpak                                                 |
|--------|--------------------------------|--------------------------------------------------------|
| 200    | OK                             | Verwerk data                                           |
| 400    | Bad Request                    | Controleer missende/ongeldige velden                   |
| 401    | Unauthorized                   | Check API‑sleutel in `Authorization` header            |
| 405    | Rate Limited                   | Wacht ⏱️ (exponential backoff)                         |
| 413    | Content Too Large              | Verkort prompt/lyrics                                  |
| 429    | Insufficient Credits           | Toon melding / schakel upgrademogelijkheid in          |
| 5xx    | Server Error                   | Log & retry met backoff                                |

### Best practices
- Valideer promptlengte (< 400 tekens) vóór verzenden.  
- Implementeer **rate limiting** in je app (bv. max 1 generatie/min).  
- Overweeg **asynchrone** aanpak met `callback_url` bij langere taken.  
- Bewaar en toon **remaining credits** via het account‑endpoint.

## Conclusie
Met de Suno API kun je eenvoudig AI‑muziek genereren in je eigen dashboard. Dit document geeft alle essentiële parameters, voorbeeldcode en best practices om veilig, efficiënt en fouttolerant met de API te werken. Ga creatief aan de slag en bouw jouw persoonlijke AI‑song‑generator!
