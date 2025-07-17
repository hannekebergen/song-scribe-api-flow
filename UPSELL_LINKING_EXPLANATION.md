# 🔗 UpSell Linking - Hoe het werkt

## 📋 Overzicht

De UpSell linking zorgt ervoor dat **UpSell orders** (zoals "Extra Coupletten" of "Soundtrack & Songtekst Bundel") automatisch gelinkt worden aan hun **originele orders** (zoals "Persoonlijk Lied - Binnen 72 uur").

## 🎯 Het Probleem

### **Waarom UpSell Linking nodig is:**
- UpSell orders hebben **geen eigen thema informatie** (klanten vullen geen nieuwe gegevens in)
- UpSell orders hebben **geen eigen songtekst** (ze bouwen voort op bestaande songtekst)
- Zonder linking kunnen we **niet zien** welke originele order bij een UpSell hoort

### **Voorbeeld:**
```
Originele Order #13297129: "Persoonlijk Lied voor Steven De Pau"
├── Thema: "Verjaardag"
├── Songtekst: "🎵 Happy Birthday to you..."
└── Besteldatum: 2025-07-16 23:38:41

UpSell Order #13297136: "Extra Coupletten voor Steven De Pau"
├── Thema: "Onbekend" ❌
├── Songtekst: "Geen" ❌
└── Besteldatum: 2025-07-16 23:39:59

Na Linking:
UpSell Order #13297136: "Extra Coupletten voor Steven De Pau"
├── Thema: "Verjaardag" ✅ (overgenomen)
├── Songtekst: "🎵 Happy Birthday to you..." ✅ (gesynchroniseerd)
├── Origin Song ID: 13297129 ✅ (gelinkt)
└── Besteldatum: 2025-07-16 23:39:59
```

---

## 🔧 Hoe de Linking Werkt

### **Stap 1: Identificeer UpSell Orders**
```python
# Check of dit een UpSell order is
for product in order.raw_data["products"]:
    pivot_type = product.get("pivot", {}).get("type")
    if pivot_type == "upsell":
        is_upsell = True
        break
```

**UpSell Product IDs:**
- **299107**: "Soundtrack & Songtekst Bundel"
- **299088**: "2 Extra Coupletten"
- **294847**: "Aanpassing na ontvangst" / "Revisie"

### **Stap 2: Zoek Klant Informatie**
```python
# Probeer email uit verschillende velden
customer_email = (
    upsell_order_data.get("customer", {}).get("email") or
    upsell_order_data.get("address", {}).get("email")
)

# Probeer naam uit verschillende velden
customer_name = (
    upsell_order_data.get("address", {}).get("full_name") or
    upsell_order_data.get("customer", {}).get("name") or
    f"{firstname} {lastname}".strip()
)
```

### **Stap 3: Zoek Originele Orders**
```python
# Zoek 7 dagen terug vanaf de UpSell order
search_start = upsell_datetime - timedelta(days=7)

# Query voor potentiële originele orders
query = db_session.query(Order).filter(
    Order.bestel_datum >= search_start,
    Order.bestel_datum < upsell_datetime,
    Order.order_id != upsell_order_id  # Niet de UpSell order zelf
)
```

### **Stap 4: Matching Strategie**

#### **A. Email Matching (Prioriteit 1)**
```python
if customer_email:
    query = query.filter(Order.klant_email == customer_email)
```

#### **B. Naam Matching (Prioriteit 2)**
```python
if not original_orders and customer_name:
    name_query = query.filter(
        (Order.klant_naam.ilike(f"%{customer_name}%")) |
        (Order.voornaam.ilike(f"%{customer_name.split()[0]}%")) |
        (Order.klant_naam.ilike(f"%{customer_name.split()[0]}%"))
    )
```

### **Stap 5: Filter op Originele Orders**
```python
# Alleen standaard orders (geen UpSell orders)
for product in order.raw_data["products"]:
    product_id = product.get("id")
    pivot_type = product.get("pivot", {}).get("type")
    
    # Standaard orders: 274588 (72u) of 289456 (24u)
    if product_id in [274588, 289456] and pivot_type != "upsell":
        original_orders.append(order)
```

### **Stap 6: Selecteer Beste Match**
```python
# Selecteer de meest recente originele order
original_order = max(original_orders, key=lambda o: o.bestel_datum)
```

---

## 📊 Praktisch Voorbeeld

### **Scenario: Steven De Pau**

**Originele Order #13297129:**
```json
{
  "order_id": 13297129,
  "klant_naam": "Steven De Pau",
  "klant_email": null,
  "bestel_datum": "2025-07-16T23:38:41",
  "thema": "Verjaardag",
  "products": [
    {
      "id": 274588,
      "name": "Persoonlijk Lied - Binnen 72 uur",
      "pivot": {"type": null}
    }
  ]
}
```

**UpSell Order #13297136:**
```json
{
  "order_id": 13297136,
  "klant_naam": "Steven De Pau",
  "klant_email": null,
  "bestel_datum": "2025-07-16T23:39:59",
  "thema": "Onbekend",
  "products": [
    {
      "id": 299088,
      "name": "2 Extra Coupletten",
      "pivot": {"type": "upsell"}
    }
  ]
}
```

### **Linking Proces:**

1. **Identificeer UpSell:** `pivot.type = "upsell"` ✅
2. **Klant Info:** `customer_name = "Steven De Pau"` ✅
3. **Zoek Periode:** 7 dagen terug vanaf 2025-07-16 23:39:59
4. **Naam Matching:** 
   - `klant_naam LIKE "%Steven De Pau%"`
   - `voornaam LIKE "%Steven%"`
   - `klant_naam LIKE "%Steven%"`
5. **Filter Originele:** `product_id = 274588` en `pivot.type != "upsell"`
6. **Beste Match:** Order #13297129 (meest recent)
7. **Link:** `origin_song_id = 13297129`
8. **Thema Overname:** `thema = "Verjaardag"`

---

## 🎯 Resultaat

### **Voor de Linking:**
```
UpSell Order #13297136:
├── Thema: "Onbekend" ❌
├── Origin Song ID: null ❌
└── Songtekst: "Geen" ❌
```

### **Na de Linking:**
```
UpSell Order #13297136:
├── Thema: "Verjaardag" ✅
├── Origin Song ID: 13297129 ✅
└── Songtekst: "🎵 Happy Birthday..." ✅ (na synchronisatie)
```

---

## 🔄 Automatische Synchronisatie

### **Wanneer je een songtekst opslaat:**
```python
# In originele order
order.songtekst = "Nieuwe songtekst..."
db.commit()

# Automatische synchronisatie naar UpSell orders
await sync_songtext_to_upsells(db, order_id, "Nieuwe songtekst...")
```

### **Synchronisatie Logica:**
```python
# Zoek alle UpSell orders die gelinkt zijn
upsell_orders = db.query(Order).filter(
    Order.origin_song_id == original_order_id
).all()

# Update alleen orders zonder eigen songtekst
for upsell_order in upsell_orders:
    if not upsell_order.songtekst or upsell_order.songtekst.strip() == "":
        upsell_order.songtekst = songtext
```

---

## 📈 Statistieken

### **Huidige Resultaten:**
- **80 orders verwerkt**
- **28 orders gelinkt** (35%)
- **27 thema's overgenomen**
- **0 fouten**

### **Waarom niet alle orders gelinkt:**
1. **Geen originele order gevonden** in zoekperiode
2. **Geen klant informatie** beschikbaar
3. **Geen standaard orders** van dezelfde klant
4. **Al gelinkt** (origin_song_id al ingesteld)

---

## 🛠️ Technische Details

### **Database Schema:**
```sql
ALTER TABLE orders ADD COLUMN origin_song_id INTEGER;
ALTER TABLE orders ADD CONSTRAINT fk_orders_origin_song_id 
    FOREIGN KEY (origin_song_id) REFERENCES orders (order_id);
CREATE INDEX idx_orders_origin_song_id ON orders (origin_song_id);
```

### **API Endpoints:**
```bash
# Voer UpSell linking uit
POST /orders/link-upsell-orders

# Haal originele songtekst op
GET /orders/{order_id}/original-songtext

# Update songtekst met synchronisatie
PUT /orders/{order_id}/songtext
```

### **Frontend Indicatoren:**
- 🟢 **"Gesynchroniseerd"** - UpSell order gelinkt
- 🔄 **"Synchroniseren..."** - Bezig met synchronisatie
- ⚠️ **"Niet gelinkt"** - UpSell order niet gelinkt
- ❌ **"Fout"** - Synchronisatie mislukt

---

## 🎉 Voordelen

### **Voor Gebruikers:**
- ✅ **Geen dubbele werkzaamheden**
- ✅ **Altijd up-to-date songteksten**
- ✅ **Duidelijke status indicatoren**
- ✅ **Efficiënte workflow**

### **Voor Systeem:**
- ✅ **Automatische synchronisatie**
- ✅ **Intelligente updates**
- ✅ **Performance optimalisatie**
- ✅ **Error handling**

### **Voor Business:**
- ✅ **Minder fouten** in songteksten
- ✅ **Snellere order processing**
- ✅ **Betere klanttevredenheid**
- ✅ **Efficiëntere workflow**

---

**🎯 Resultaat: UpSell orders worden nu automatisch gelinkt aan originele orders, waardoor songtekst synchronisatie mogelijk wordt!** 