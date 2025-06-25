# Plug&Pay API Data Structuur Analyse

## Overzicht
Gebaseerd op echte API data van 25 orders opgehaald op 2025-06-25.

## Hoofdstructuur Order
```json
{
  "id": 13052893,
  "products": [...],
  "address": {...},
  "created_at": "2025-06-24 22:59:40",
  "payment_status": "paid",
  "total": 29.99,
  // ... meer velden
}
```

## Belangrijke Bevindingen

### 1. **Custom Fields Locatie**
❌ **NIET op root niveau** - geen `custom_field_inputs` in de hoofdorder
✅ **WEL in products** - `products[0].custom_field_inputs`

### 2. **Custom Fields Structuur**
```json
{
  "id": 789014,
  "label": "Beschrijf",
  "input": "Lange beschrijving tekst...",
  "product_id": 274588,
  "public_label": "Voor wie? Welk gevoel? Herinneringen? Muziekstijl?"
}
```

**Veld mapping:**
- `label` = interne naam (bijv. "Beschrijf", "Vertel over de gelegenheid")
- `input` = de werkelijke waarde/tekst van de klant
- `public_label` = label zoals getoond aan klant

### 3. **Klantinformatie**
```json
"address": {
  "email": "avdberg2000@gmail.com",
  "firstname": "Angelique",
  "lastname": "van den Berg",
  "full_name": "Angelique van den Berg",
  "telephone": "0657998498"
}
```

### 4. **Product Types & IDs**
- **274588** = "Persoonlijk Lied - Binnen 72 uur" (Standaard)
- **299107** = "Soundtrack & Songtekst Bundel" (Upsell)
- **289456** = Spoed 24u (verwacht, niet gezien in sample)

### 5. **Pivot Types**
- `pivot.type: null` = Hoofdproduct
- `pivot.type: "upsell"` = Upsell product
- `pivot.type: "order-bump"` = Add-on product

## Verschillen met Huidige Implementatie

### Backend Issues
1. **Custom Fields Extractie** - Huidige code zoekt op root niveau, maar fields zitten in `products[].custom_field_inputs`
2. **Field Names** - Echte veldnamen: "Beschrijf", "Vertel over de gelegenheid"
3. **Data Mapping** - `input` veld bevat de waarde, niet `value`

### Frontend Issues  
1. **Type Detection** - Product ID 299107 heeft `pivot.type: "upsell"`
2. **Customer Name** - `address.full_name` is beschikbaar en correct
3. **Field Structure** - Andere structuur dan verwacht in types

## Aanbevelingen

### 1. **Backend Fixes**
```python
# In app/services/plugpay_client.py
def get_custom_fields(order_data):
    custom_fields = {}
    
    # Check products voor custom_field_inputs
    for product in order_data.get("products", []):
        for field in product.get("custom_field_inputs", []):
            label = field.get("label")
            value = field.get("input")  # Niet 'value'!
            if label and value:
                custom_fields[label] = value
    
    return custom_fields
```

### 2. **Schema Updates**
```python
# In app/schemas/order.py
def derive_fields(cls, values):
    raw = values.get("raw_data") or {}
    
    # Extract from products.custom_field_inputs
    for product in raw.get("products", []):
        for field in product.get("custom_field_inputs", []):
            label = field.get("label")
            value = field.get("input")
            
            if label == "Beschrijf":
                values.setdefault("beschrijving", value)
            elif label == "Vertel over de gelegenheid":
                values.setdefault("thema", value)
```

### 3. **Frontend Type Updates**
```typescript
// In src/types.ts
interface CustomFieldInput {
  id: number;
  label: string;
  input: string;  // Niet 'value'
  product_id: number;
  public_label: string;
}

interface Product {
  id: number;
  title: string;
  custom_field_inputs: CustomFieldInput[];
  pivot: {
    type: string | null;
    quantity: number;
    // ...
  };
}
```

## Test Data Voorbeelden

### Order 13052893 (Standaard)
- Product: 274588 "Persoonlijk Lied - Binnen 72 uur"
- Pivot type: `null`
- Custom fields: "Beschrijf", "Vertel over de gelegenheid"
- Klant: "Angelique van den Berg"

### Order 13047563 (Upsell)  
- Product: 299107 "Soundtrack & Songtekst Bundel"
- Pivot type: `"upsell"`
- Custom fields: 0 (lege array)
- Klant: "Helma Hoek"

## Volgende Stappen

1. ✅ **API Data Analyse** - Compleet
2. 🔄 **Backend Custom Fields Fix** - Update plugpay_client.py
3. 🔄 **Schema Updates** - Fix field extraction
4. 🔄 **Frontend Types** - Update interfaces
5. 🔄 **Order Type Detection** - Fix product ID mapping
6. 🔄 **Testing** - Valideer met echte data 