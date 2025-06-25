# Order Type Detectie Implementatie

## Overzicht

Deze implementatie voegt intelligente order type detectie toe aan het Song-Scribe dashboard. Het systeem kan nu automatisch verschillende soorten orders onderscheiden op basis van product informatie van de Plug&Pay API.

## Ondersteunde Order Types

| Type | Product ID | Kenmerk | Badge | Prioriteit |
|------|------------|---------|-------|------------|
| **Spoed 24u** | 289456 | `products[0].id == 289456` | 🚀 Spoed 24u | 200 |
| **Standaard 72u** | 274588 | `products[0].id == 274588` | 📝 Standaard 72u | 100 |
| **Upsell - Revisie** | 294847 | `products[*].pivot.type == "upsell"` | ⬆️ Upsell | 50 |
| **Upsell - Soundtrack** | 299107 | `products[*].pivot.type == "upsell"` | ⬆️ Upsell | 50 |
| **Upsell - Extra Coupletten** | 299088 | `products[*].pivot.type == "upsell"` | ⬆️ Upsell | 50 |
| **Order-bump - Karaoke** | 294792 | `products[*].pivot.type == "order-bump"` | ➕ Add-on | 30 |
| **Order-bump - Engelstalig** | 299891 | `products[*].pivot.type == "order-bump"` | ➕ Add-on | 30 |

## Implementatie Details

### 1. Frontend Implementatie

#### **Nieuwe Utility (`src/utils/orderTypeDetection.ts`)**
```typescript
export function detectOrderType(order: Order): OrderTypeInfo {
  // Analyseert producten en pivot types
  // Bepaalt hoofdtype op basis van prioriteit
  // Combineert meerdere types indien nodig
}
```

**Belangrijke functies:**
- `detectOrderType()` - Hoofddetectie logica
- `getOrderTypeDisplay()` - Display string voor UI
- `getOrderTypeBadge()` - Badge type voor styling
- `isSpeedOrder()` - Check voor spoed orders

#### **Updated useFetchOrders Hook**
- Gebruikt nieuwe order type detectie
- Intelligente deadline detectie gebaseerd op order type
- Verbeterde debug logging

#### **Enhanced OrdersTable Component**
- Nieuwe badge styling voor verschillende types
- Gecombineerde type weergave (bijv. "Standaard 72u + Engelstalig")
- Visuele onderscheiding tussen hoofdtypes en add-ons

### 2. Backend Implementatie

#### **Updated Order Schema (`app/schemas/order.py`)**
```python
def detect_order_type(raw_data: dict) -> str:
    # Analyseert product informatie
    # Bepaalt type op basis van ID en pivot type
    # Combineert meerdere types met prioriteit
```

**Nieuwe velden:**
- `typeOrder: Optional[str]` - Gedetecteerd order type

#### **Database Migration**
- Nieuwe `typeOrder` kolom toegevoegd aan orders tabel
- Migration: `ac5c3189725c_add_typeorder_and_persoonlijk_verhaal_to_orders`

#### **Updated Types (`src/types.ts`)**
- Uitgebreide product interface met `id`, `pivot`, etc.
- Ondersteuning voor beide legacy en nieuwe formaten

### 3. Detectie Logica

#### **Prioriteit Systeem**
1. **Spoed 24u** (prioriteit 200) - Hoogste prioriteit
2. **Standaard 72u** (prioriteit 100) - Basis product
3. **Upsells** (prioriteit 50) - Extra services
4. **Order-bumps** (prioriteit 30) - Add-ons

#### **Fallback Mechanisme**
- Product ID matching (primair)
- Pivot type analysis (secundair)
- Title/naam analyse (tertiair)
- Onbekend type (fallback)

#### **Combinatie Logica**
- Hoofdtype wordt bepaald door hoogste prioriteit
- Andere types worden toegevoegd als "+ Extra Type"
- Voorbeeld: "Standaard 72u + Engelstalig"

## Test Resultaten

Getest met echte API data:

```
Order 13052893: Standaard 72u
  - Product 274588 (Persoonlijk Lied - Binnen 72 uur): pivot=None

Order 13047549: Standaard 72u + Engelstalig  
  - Product 274588 (Persoonlijk Lied - Binnen 72 uur): pivot=None
  - Product 299891 (Engelstalig): pivot=order-bump

Order 13047563: Soundtrack Bundel
  - Product 299107 (Soundtrack & Songtekst Bundel): pivot=upsell
```

## Dashboard Verbeteringen

### **Visuele Indicatoren**
- 🚀 **Rood badge** voor spoed orders
- 📝 **Blauw badge** voor standaard orders  
- ⬆️ **Paars badge** voor upsells
- ➕ **Groen badge** voor add-ons

### **Filtering & Sorting**
- Orders kunnen gefilterd worden op type
- Spoed orders krijgen visuele prioriteit
- Gecombineerde types worden correct weergegeven

### **Deadline Detectie**
- Automatische 24u deadline voor spoed orders
- Standaard 72u voor normale orders
- Custom deadlines uit formulier velden

## Extensibiliteit

Het systeem is ontworpen voor eenvoudige uitbreiding:

1. **Nieuwe Product Types**: Voeg toe aan detectie functies
2. **Nieuwe Badges**: Definieer in badge mapping
3. **Nieuwe Prioriteiten**: Pas prioriteit systeem aan
4. **Nieuwe Combinaties**: Logica ondersteunt automatisch

## Bestandsoverzicht

### **Aangepaste Bestanden:**
- `src/utils/orderTypeDetection.ts` (NIEUW)
- `src/hooks/useFetchOrders.ts` (UPDATED)
- `src/components/dashboard/OrdersTable.tsx` (UPDATED)
- `src/types.ts` (UPDATED)
- `app/schemas/order.py` (UPDATED)
- `app/models/order.py` (UPDATED)

### **Database Wijzigingen:**
- Nieuwe `typeOrder` kolom in orders tabel
- Migration script voor database upgrade

## Conclusie

De implementatie biedt een robuust en uitbreidbaar systeem voor order type detectie dat:

✅ **Automatisch** verschillende order types herkent  
✅ **Visueel** onderscheid maakt in het dashboard  
✅ **Intelligent** prioriteiten toepast  
✅ **Flexibel** is voor nieuwe types  
✅ **Backward compatible** blijft met bestaande data  

Het dashboard geeft nu een veel duidelijker overzicht van de verschillende soorten orders en hun urgentie. 