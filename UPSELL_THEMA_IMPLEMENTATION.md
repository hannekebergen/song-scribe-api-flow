# UpSell Thema Inheritance - Implementatie Documentatie

## Overzicht

Deze implementatie lost twee belangrijke problemen op:
1. **Klantnaam weergave**: De klantnaam wordt nu correct weergegeven in het orders tabel onder de kolom "Klant"
2. **UpSell thema inheritance**: UpSell orders nemen automatisch het thema over van hun originele order

## Problemen Geanalyseerd

### Probleem 1: UpSell Orders Zonder Thema
UpSell orders (zoals "2 Extra Coupletten" en "Soundtrack & Songtekst Bundel") hebben lege `custom_field_inputs` arrays omdat klanten geen nieuwe thema informatie invullen - ze bouwen voort op een bestaande order.

### Probleem 2: Geen Link naar Originele Order
Er was geen mechanisme om te identificeren welke originele order bij een UpSell hoort.

## Implementatie Details

### 1. Database Wijzigingen

#### Nieuwe Migratie: `add_origin_song_id_to_orders.py`
```sql
-- Voegt origin_song_id veld toe voor linking van UpSell orders
ALTER TABLE orders ADD COLUMN origin_song_id INTEGER;

-- Foreign key constraint naar originele order
ALTER TABLE orders ADD CONSTRAINT fk_orders_origin_song_id 
    FOREIGN KEY (origin_song_id) REFERENCES orders (order_id);

-- Index voor performance
CREATE INDEX idx_orders_origin_song_id ON orders (origin_song_id);
```

#### Order Model Update
```python
# app/models/order.py
origin_song_id = Column(Integer, nullable=True)  # Voor UpSell orders
```

### 2. Backend Logica

#### Nieuwe Service: `app/services/upsell_linking.py`
- **`find_original_order_for_upsell()`**: Vindt de originele order voor een UpSell
- **`inherit_theme_from_original()`**: Neemt thema over van originele order

#### Linking Strategie
1. Zoek orders van dezelfde klant (email/naam) binnen 24 uur voor de UpSell
2. Filter op standaard orders (product_id 274588 of 289456)
3. Selecteer de meest recente match
4. Link de UpSell order en neem thema over

#### Automatische Linking in Order Creation
```python
# app/models/order.py - create_from_plugpay_data()
if is_upsell:
    original_order_id = find_original_order_for_upsell(db_session, order_data)
    if original_order_id:
        new_order.origin_song_id = original_order_id
        if not new_order.thema:
            inherit_theme_from_original(db_session, new_order, original_order_id)
```

#### Nieuwe API Endpoint
```python
# app/routers/orders.py
@router.post("/link-upsell-orders")
async def link_upsell_orders():
    """Link bestaande UpSell orders aan hun originele orders"""
```

### 3. Frontend Wijzigingen

#### TypeScript Types Update
```typescript
// src/types.ts
export interface Order {
    // ... existing fields
    origin_song_id?: number;
}
```

#### Enhanced Thema Extraction
```typescript
// src/hooks/useFetchOrders.ts
const getThema = (): string => {
    // 1. Probeer backend thema veld
    // 2. Probeer custom fields
    // 3. Voor UpSell orders: zoek originele order en neem thema over
    // 4. Fallback naar 'Onbekend'
}
```

#### Intelligente Fallback Logic
- Als UpSell order geen thema heeft, zoek naar originele order via `origin_song_id`
- Als geen directe link, zoek op klant naam en datum (binnen 24 uur)
- Toon duidelijk dat thema is overgenomen: "(van originele order)" of "(overgenomen)"

### 4. Orders Tabel Display

De orders tabel toont nu correct:
- **Ordernummer**: Unieke order ID
- **Type Order**: Badge met order type (Standaard, Spoed, UpSell, etc.)
- **Datum**: Besteldatum
- **Thema**: Met inheritance voor UpSell orders
- **Klant**: Klantnaam (was al correct ingesteld)
- **Status**: Prompt status
- **Acties**: Bekijk knop

## Testing & Validatie

### Test Script: `test_upsell_linking.py`
```bash
# Test de nieuwe functionaliteit
python test_upsell_linking.py
```

### API Endpoint Test
```bash
# Link bestaande UpSell orders
curl -X POST "http://localhost:8000/api/orders/link-upsell-orders" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

## Resultaten

### Voor de Implementatie
- UpSell orders hadden geen thema ("Onbekend")
- Geen link tussen UpSell en originele orders
- Moeilijk te zien welke orders bij elkaar horen

### Na de Implementatie
- ✅ UpSell orders tonen thema van originele order
- ✅ Database links tussen UpSell en originele orders
- ✅ Frontend toont duidelijk overgenomen thema's
- ✅ Automatische linking voor nieuwe orders
- ✅ Batch processing voor bestaande orders

## Product ID Mapping

### Standaard Orders
- **274588**: "Persoonlijk Lied - Binnen 72 uur" (Standaard)
- **289456**: "Spoed 24u" (Rush)

### UpSell Orders
- **299107**: "Soundtrack & Songtekst Bundel" (pivot.type: "upsell")
- **299088**: "2 Extra Coupletten" (pivot.type: "upsell")
- **294847**: "Aanpassing na ontvangst" / "Revisie" (pivot.type: "upsell")

## Monitoring & Logging

Alle linking activiteiten worden gelogd met details over:
- Welke orders zijn gelinkt
- Welke thema's zijn overgenomen
- Eventuele fouten of waarschuwingen

## Toekomstige Verbeteringen

1. **UI Indicator**: Visuele indicator in dashboard voor gelinkte orders
2. **Bulk Operations**: Bulk edit functionaliteit voor thema's
3. **Analytics**: Rapportage over UpSell success rates
4. **Auto-refresh**: Automatische refresh van thema's bij wijzigingen

## Deployment Checklist

- [x] Database migratie uitgevoerd
- [x] Backend code gedeployed
- [x] Frontend code gedeployed
- [x] API endpoints getest
- [x] Bestaande orders gelinkt via batch endpoint
- [x] Frontend thema display gevalideerd 