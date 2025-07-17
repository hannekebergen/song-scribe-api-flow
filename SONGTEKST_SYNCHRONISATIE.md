# 🎵 Songtekst Synchronisatie - UpSell Orders

## 📋 Overzicht

Deze implementatie zorgt ervoor dat wanneer je een **songtekst opslaat** in een **originele order**, deze automatisch **zichtbaar wordt** in alle bijbehorende **UpSell orders**.

## 🎯 Het Probleem

### **Voor de implementatie:**
```
1. Originele Order → Songtekst opslaan ✅
2. UpSell Order → Originele songtekst niet zichtbaar ❌
3. Gebruiker moet handmatig zoeken naar originele order ❌
4. Dubbele werkzaamheden en fouten ❌
```

### **Na de implementatie:**
```
1. Originele Order → Songtekst opslaan ✅
2. UpSell Order → Originele songtekst automatisch zichtbaar ✅
3. Synchronisatie status duidelijk aangegeven ✅
4. Efficiënte workflow ✅
```

---

## 🚀 Nieuwe Functionaliteit

### **1. Automatische Synchronisatie**

Wanneer je een songtekst opslaat in een originele order:

```python
# Backend: Automatische synchronisatie
@router.put("/{order_id}/songtext")
async def update_songtext(order_id: int, songtext_update: UpdateSongtextRequest):
    # Update originele order
    order.songtekst = songtext_update.songtekst
    db.commit()
    
    # SYNCHRONISEER NAAR UPSELL ORDERS
    await sync_songtext_to_upsells(db, order_id, songtext_update.songtekst)
```

### **2. Intelligente Synchronisatie**

De synchronisatie is **intelligent**:
- ✅ Synchroniseert alleen naar UpSell orders **zonder eigen songtekst**
- ✅ Overschrijft **niet** bestaande songteksten in UpSell orders
- ✅ Behoudt **werk van gebruikers** in UpSell orders

### **3. Frontend Indicatoren**

De frontend toont duidelijk:
- 🔄 **Synchronisatie status** (idle/syncing/synced/error)
- 📋 **Originele songtekst** in aparte card
- 🔗 **Link naar originele order** informatie
- 💾 **"Opslaan & Synchroniseren"** knop

---

## 🛠️ Technische Implementatie

### **Backend API Endpoints**

#### **PUT /orders/{order_id}/songtext**
```json
{
  "songtekst": "Nieuwe songtekst...",
  "sync_to_upsells": true
}
```

**Response:**
```json
{
  "id": 123,
  "order_id": 13052893,
  "songtekst": "Nieuwe songtekst...",
  "klant_naam": "Jan Jansen",
  "thema": "Verjaardag",
  // ... andere order velden
}
```

#### **GET /orders/{order_id}/original-songtext**
Haalt originele songtekst op voor UpSell orders.

**Response:**
```json
{
  "success": true,
  "original_songtext": "Originele songtekst...",
  "original_order_id": 13052893,
  "upsell_order_id": 13052894,
  "original_order_info": {
    "klant_naam": "Jan Jansen",
    "thema": "Verjaardag",
    "bestel_datum": "2025-01-27T10:00:00"
  }
}
```

### **Database Schema**

```sql
-- Orders tabel met origin_song_id voor UpSell linking
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL,
    songtekst TEXT,
    origin_song_id INTEGER REFERENCES orders(order_id),
    -- ... andere velden
);

-- Index voor performance
CREATE INDEX idx_orders_origin_song_id ON orders (origin_song_id);
```

### **Frontend Components**

#### **UpsellSongEditor**
```typescript
interface UpsellSongEditorProps {
  order: Order;
  onOrderUpdate: (order: Order) => void;
}

const UpsellSongEditor: React.FC<UpsellSongEditorProps> = ({ order, onOrderUpdate }) => {
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'synced' | 'error'>('idle');
  
  // Automatische synchronisatie bij opslaan
  const handleSave = async () => {
    const updatedOrder = await ordersApi.updateSongtext(order.order_id, editedSongtext);
    onOrderUpdate(updatedOrder);
    setSyncStatus('synced');
  };
  
  // Handmatige synchronisatie van originele songtekst
  const handleSyncFromOriginal = async () => {
    const updatedOrder = await ordersApi.updateSongtext(order.order_id, originalSongtext);
    setEditedSongtext(originalSongtext);
    onOrderUpdate(updatedOrder);
  };
};
```

---

## 🎨 User Experience

### **Voor Originele Orders**
1. **Bewerk songtekst** zoals gewoonlijk
2. **Klik "Opslaan"** 
3. **Automatische synchronisatie** naar UpSell orders
4. **Bevestiging** dat synchronisatie is gelukt

### **Voor UpSell Orders**
1. **Open UpSell order** detail pagina
2. **Zie originele songtekst** in aparte card
3. **Bewerk songtekst** of synchroniseer van origineel
4. **Klik "Opslaan & Synchroniseren"**
5. **Status indicatoren** tonen synchronisatie status

### **Visuele Indicatoren**
- 🟢 **Groen badge**: "Gesynchroniseerd"
- 🔄 **Spinner**: Synchronisatie bezig
- ⚠️ **Oranje badge**: "Niet opgeslagen"
- ❌ **Rood badge**: Synchronisatie fout

---

## 🔧 Configuratie

### **Environment Variables**
```env
# Geen extra configuratie nodig
# Synchronisatie werkt automatisch
```

### **Database Migrations**
```bash
# Voer uit als nog niet gedaan:
python direct_migrations.py
```

### **API Keys**
```env
# Bestaande API key blijft hetzelfde
API_KEY=jouwsong2025
```

---

## 🧪 Testing

### **Test Script**
```bash
# Test de volledige functionaliteit
python test_songtext_sync.py
```

### **Handmatige Test**
1. **Open originele order** met songtekst
2. **Bewerk songtekst** en sla op
3. **Open bijbehorende UpSell order**
4. **Controleer** of originele songtekst zichtbaar is
5. **Test synchronisatie** knop

### **API Test**
```bash
# Test synchronisatie endpoint
curl -X PUT "http://localhost:8000/orders/13052893/songtext" \
  -H "X-API-Key: jouwsong2025" \
  -H "Content-Type: application/json" \
  -d '{
    "songtekst": "Nieuwe test songtekst...",
    "sync_to_upsells": true
  }'
```

---

## 📊 Monitoring & Logging

### **Backend Logs**
```
INFO: Songtekst gesynchroniseerd naar UpSell order 13052894
INFO: Songtekst gesynchroniseerd naar 2 UpSell orders voor originele order 13052893
INFO: Geen UpSell orders bijgewerkt (alleen orders zonder bestaande songtekst)
```

### **Frontend Console**
```
✅ Songtekst opgeslagen en automatisch gesynchroniseerd naar UpSell orders
✅ Songtekst gesynchroniseerd van originele order
⚠️ Order niet gelinkt - voer eerst linking proces uit
```

---

## 🚨 Troubleshooting

### **"Order niet gelinkt"**
```bash
# Voer UpSell linking uit
curl -X POST "http://localhost:8000/orders/link-upsell-orders" \
  -H "X-API-Key: jouwsong2025"
```

### **"Synchronisatie werkt niet"**
1. **Check database** voor `origin_song_id` velden
2. **Check logs** voor foutmeldingen
3. **Test API endpoints** handmatig
4. **Verifieer** dat UpSell orders gelinkt zijn

### **"Originele songtekst niet gevonden"**
1. **Check** of originele order een songtekst heeft
2. **Check** of `origin_song_id` correct is ingesteld
3. **Test** `/orders/{id}/original-songtext` endpoint

---

## 🎯 Voordelen

### **Voor Gebruikers**
- ✅ **Geen dubbele werkzaamheden** meer
- ✅ **Altijd up-to-date** songteksten
- ✅ **Duidelijke status** indicatoren
- ✅ **Efficiënte workflow**

### **Voor Systeem**
- ✅ **Automatische synchronisatie**
- ✅ **Intelligente updates** (geen overschrijving)
- ✅ **Performance optimalisatie**
- ✅ **Error handling** en logging

### **Voor Business**
- ✅ **Minder fouten** in songteksten
- ✅ **Snellere order processing**
- ✅ **Betere klanttevredenheid**
- ✅ **Efficiëntere workflow**

---

## 🔮 Toekomstige Uitbreidingen

### **Geplande Features**
- 🔄 **Real-time synchronisatie** via WebSockets
- 📧 **Email notificaties** bij synchronisatie
- 📊 **Synchronisatie analytics** en rapporten
- 🔒 **Granular permissions** voor synchronisatie

### **Mogelijke Verbeteringen**
- 🎨 **Diff view** tussen originele en UpSell songteksten
- 🔄 **Bulk synchronisatie** voor meerdere orders
- 📱 **Mobile notifications** voor synchronisatie status
- 🤖 **AI-powered** songtekst uitbreidingen

---

## 📞 Support

### **Bij Problemen**
1. **Check logs** voor foutmeldingen
2. **Test API endpoints** handmatig
3. **Verifieer database** schema
4. **Run test script** voor diagnose

### **Contact**
- **Backend issues**: Check `app/routers/orders.py`
- **Frontend issues**: Check `src/components/order-detail/UpsellSongEditor.tsx`
- **Database issues**: Check `alembic/versions/` migrations

---

**🎉 Implementatie voltooid! Je songtekst synchronisatie werkt nu automatisch tussen originele en UpSell orders.** 