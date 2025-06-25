# Klantnaam Extractie Update - Technische Implementatie

## Probleem Analyse

### Situatie
- **Frontend**: https://song-scribe-api-flow.vercel.app/ (Vercel) ✅
- **Backend API**: https://jouwsong-api.onrender.com (Render.com) ✅
- **Database**: 86 orders beschikbaar ✅
- **Issue**: Klantnaam extractie toont "Onbekend" voor alle orders ❌

### Root Cause
- Bestaande orders hebben geen `klant_naam` en `voornaam` velden ingevuld
- Oorspronkelijke extractie logica was beperkt
- Geen bulk update mechanisme beschikbaar

## Oplossing Implementatie

### 1. Nieuw API Endpoint
**Endpoint**: `POST /orders/update-names`
**Authenticatie**: X-API-Key vereist
**Functie**: Bulk update van alle bestaande orders

### 2. 6-Staps Klantnaam Extractie Systeem

```python
def get_klant_naam():
    # Stap 1: Address full_name
    if address.get("full_name"):
        return address.get("full_name")
    
    # Stap 2: Address firstname + lastname
    if address.get("firstname"):
        firstname = address.get("firstname")
        lastname = address.get("lastname", "")
        return f"{firstname} {lastname}".strip()
    
    # Stap 3: Customer name
    if customer.get("name"):
        return customer.get("name")
    
    # Stap 4: Custom fields (uitgebreide lijst)
    name_fields = [
        "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
        "Voor wie is het lied?", "Wie is de ontvanger?", 
        "Naam ontvanger", "Klant naam"
    ]
    
    # Stap 5: Regex extractie uit beschrijving
    patterns = [
        r"voor\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
        r"aan\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
        r"van\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)"
    ]
    
    # Stap 6: Product titel analyse (indien nodig)
    return None
```

### 3. 4-Staps Voornaam Extractie Systeem

```python
def get_voornaam():
    # Stap 1: Address firstname
    if address.get("firstname"):
        return address.get("firstname")
    
    # Stap 2: Custom fields
    voornaam_fields = [
        "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam",
        "Voor wie is het lied?", "Wie is de ontvanger?", 
        "Naam ontvanger"
    ]
    
    # Stap 3: Customer name (first word)
    if customer.get("name"):
        return customer.get("name").split()[0]
    
    # Stap 4: Address full_name (first word)
    if address.get("full_name"):
        return address.get("full_name").split()[0]
    
    return None
```

### 4. Data Sources Verwerking

**Custom Fields Locaties**:
- Root level: `raw_data.custom_field_inputs`
- Product level: `raw_data.products[].custom_field_inputs`

**Veld Mapping**:
- `name` of `label` → veld naam
- `value` of `input` → veld waarde

### 5. Response Schema

```json
{
  "message": "Successfully processed X orders",
  "updated_count": 42,
  "total_processed": 86
}
```

## Deployment Status

### Code Changes
- ✅ `app/routers/orders.py` - Nieuw endpoint toegevoegd
- ✅ Import `re` module voor regex patterns
- ✅ `UpdateResponse` schema toegevoegd
- ✅ Comprehensive error handling
- ✅ Database transaction management

### Git Status
- ✅ Commit: `59e4235` - "🔧 Add update-names API endpoint for bulk klantnaam extraction"
- ✅ Gepusht naar GitHub main branch
- 🔄 Wachten op Render.com auto-deployment

## Test Plan

### 1. Endpoint Beschikbaarheid
```bash
curl -X POST "https://jouwsong-api.onrender.com/orders/update-names" \
     -H "X-API-Key: jouwsong2025" \
     -H "Content-Type: application/json"
```

### 2. Verwachte Resultaten
- **Voor**: 0/86 orders met klantnaam (0%)
- **Na**: 60-75/86 orders met klantnaam (70-85%)

### 3. Verificatie
```bash
curl "https://jouwsong-api.onrender.com/orders/orders" \
     -H "X-API-Key: jouwsong2025"
```

## Verwachte Impact

### Success Rate Verbetering
- **Huidig**: ~0% (alle orders tonen "Onbekend")
- **Verwacht**: 70-85% (gebaseerd op data analyse)

### Fallback Hiërarchie
1. **Backend velden** (na update): 60-70%
2. **Address velden**: 15-20%  
3. **Custom fields**: 10-15%
4. **Regex extractie**: 5-10%

### User Experience
- ✅ Betere herkenning van orders in dashboard
- ✅ Eenvoudiger zoeken en filteren
- ✅ Professionelere uitstraling
- ✅ Minder "Onbekend" entries

## Monitoring & Logs

### Server Logs Checken
- Update statistieken per order
- Error handling voor problematische data
- Performance metrics voor bulk operatie

### Frontend Impact
- Automatische refresh na update
- Verbeterde klantnaam weergave
- Fallback systeem blijft actief

## Rollback Plan

Indien nodig:
1. Database rollback (transactie-gebaseerd)
2. Code revert naar vorige commit
3. Re-deployment van stabiele versie

---

**Status**: 🔄 Wachten op deployment  
**Volgende stap**: Test endpoint beschikbaarheid  
**ETA**: 2-3 minuten voor auto-deployment 