# Fixes voor Klantnaam en Order Type Problemen

## 🔍 Geïdentificeerde Problemen

### 1. Klantnaam wordt niet correct weergegeven
- **Symptoom**: Dashboard toont overal "Onbekend" en order detail toont alleen "-"
- **Oorzaak**: Backend extractie logica was te beperkt en gebruikte niet alle beschikbare data bronnen
- **Impact**: Gebruikers kunnen orders niet gemakkelijk identificeren

### 2. Order Type toont overal "Standaard 72u"
- **Symptoom**: Geen variatie in order types, alles wordt als "Standaard" geclassificeerd
- **Oorzaak**: Product ID detectie werkte niet voor alle producten, ontbrekende fallback logica
- **Impact**: Geen onderscheid tussen spoed orders en reguliere orders

## 🛠️ Geïmplementeerde Oplossingen

### Backend Verbeteringen

#### 1. Verbeterde Klantnaam Extractie (`app/models/order.py`)
```python
def get_klant_naam():
    # Hiërarchie van fallbacks:
    # 1. customer.name
    # 2. address.full_name  
    # 3. address.firstname + lastname
    # 4. Custom fields: "Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam"
    # 5. Combinatie met achternaam uit custom fields
```

**Nieuwe Custom Field Varianten:**
- "Voornaam"
- "Voor wie is dit lied?"
- "Voor wie"
- "Naam"
- "Achternaam" / "Van" (voor combinatie)

#### 2. Verbeterde Schema Verwerking (`app/schemas/order.py`)
```python
# Verbeterde voornaam extractie
if not values.get("voornaam"):
    voornaam = address.get("firstname")
    if not voornaam:
        voornaam = pick("Voornaam", "Voor wie is dit lied?", "Voor wie", "Naam")
    values.setdefault("voornaam", voornaam)

# Verbeterde klantnaam extractie als fallback
if not values.get("klant_naam"):
    # Meerdere fallback strategieën...
```

#### 3. Verbeterde Order Type Detectie (`app/schemas/order.py`)
```python
def detect_order_type(raw_data: dict) -> str:
    # Nieuwe fallback logica:
    # 1. Specifieke Product IDs (274588, 289456)
    # 2. Pivot type analyse (upsell, order-bump)
    # 3. Titel analyse met keywords
    # 4. Default naar "Standaard 72u" voor songtekst/lied producten
```

**Nieuwe Detectie Keywords:**
- "spoed" → Spoed 24u
- "standaard" → Standaard 72u
- "songtekst" of "lied" → Standaard 72u (default)

### Frontend Verbeteringen

#### 1. Verbeterde Klantnaam Mapping (`src/hooks/useFetchOrders.ts`)
```typescript
const getKlantNaam = (): string => {
    // Verbeterde checks met trim() validatie
    // Betere fallback naar custom fields
    // Robuustere error handling
}
```

#### 2. Verbeterde Order Type Detectie (`src/utils/orderTypeDetection.ts`)
```typescript
// Consistente fallback logica met backend
// Nieuwe keyword detectie voor "spoed" en "standaard"
// Default naar "Standaard 72u" voor songtekst producten
```

## 🧪 Test Scripts

### 1. `test_name_extraction.py`
Test script voor validatie van naam extractie logica met verschillende scenario's:
- Order met address.full_name
- Order met address.firstname + lastname  
- Order met custom fields voornaam
- Order met "Voor wie is dit lied?" custom field
- Order zonder naam informatie

### 2. `update_existing_orders.py`
Script om bestaande orders in database bij te werken:
- Herverwerkt alle orders met nieuwe naam extractie logica
- Update klant_naam en voornaam velden
- Logging van alle wijzigingen

## 📊 Verwachte Resultaten

### Voor Klantnaam:
- **Voor**: "Onbekend" in 80%+ van de gevallen
- **Na**: Correcte namen uit address of custom fields
- **Fallback**: Alleen "Onbekend" als er echt geen naam informatie is

### Voor Order Type:
- **Voor**: "Standaard 72u" in 100% van de gevallen
- **Na**: Correcte detectie van:
  - Spoed 24u orders
  - Standaard 72u orders  
  - Upsell producten
  - Order-bump producten
  - Intelligente fallbacks op basis van titel

## 🚀 Implementatie Stappen

1. **Backend wijzigingen zijn geïmplementeerd**
   - ✅ `app/models/order.py` - Verbeterde naam extractie
   - ✅ `app/schemas/order.py` - Verbeterde schema verwerking en order type detectie

2. **Frontend wijzigingen zijn geïmplementeerd**
   - ✅ `src/hooks/useFetchOrders.ts` - Verbeterde naam mapping
   - ✅ `src/utils/orderTypeDetection.ts` - Verbeterde type detectie

3. **Bestaande data bijwerken**
   - 🔄 Voer `update_existing_orders.py` uit om bestaande orders bij te werken
   - 🔄 Test met echte data via API call naar `/orders/fetch`

4. **Validatie**
   - 🔄 Check dashboard voor correcte klantnamen
   - 🔄 Verificeer order type variatie
   - 🔄 Test edge cases met verschillende data formaten

## 🔧 Debug Mogelijkheden

### Log Level verhogen voor debugging:
```bash
# In .env bestand
LOG_LEVEL=DEBUG
```

### Test individuele order:
```python
python test_name_extraction.py
```

### Database update uitvoeren:
```python
python update_existing_orders.py
```

## 📝 Monitoring

Na implementatie, monitor de volgende metrics:
- Percentage orders met "Onbekend" als klantnaam (moet <10% zijn)
- Variatie in order types (moet meerdere types tonen)
- Frontend error logs voor mapping issues
- Backend logs voor custom field extractie failures

## 🔄 Volgende Stappen

1. **Onmiddellijk**: Database update script uitvoeren
2. **Kort termijn**: Monitoring van resultaten in productie
3. **Middellange termijn**: Feedback verzamelen van gebruikers
4. **Lange termijn**: Eventuele verdere optimalisaties op basis van echte data patronen 