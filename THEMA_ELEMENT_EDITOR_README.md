# 🎛️ Thema Element Editor - Gebruikershandleiding

## 🚀 Wat is Nieuw?

Je kunt nu **direct via het dashboard** thema datasets bewerken! Keywords toevoegen/verwijderen, power phrases aanpassen, instrumenten wijzigen, en meer.

## 📍 Hoe Te Bereiken

1. **Dashboard** → **Thema's tab** → **Thema selecteren** → **👁️ Bekijken**
2. In het thema detail dialog → **"Bewerken" knop** (rechtsboven)

## 🎯 Functionaliteiten

### **Bekijk Modus (Standaard)**
- **Overzicht** van alle elementen gegroepeerd per type
- **Element counts** en **type beschrijvingen**
- **Logische sortering** van element types
- **Compacte weergave** met badges voor context/weight

### **Bewerkingsmodus**
Klik op **"Bewerken"** om te activeren:

#### **📝 Bestaande Elementen**
- **Inline editing**: Dubbelklik op element om te bewerken
- **Enter**: Opslaan
- **Escape**: Annuleren  
- **🗑️ Verwijderen**: Rode prullenbak-knop
- **Context & Weight**: Zichtbaar via badges

#### **➕ Nieuwe Elementen Toevoegen**
**Per Element Type:**
- **Snelle toevoeging**: Type content + Enter
- **Context selectie**: intro, verse, chorus, bridge, outro
- **Weight instelling**: 1-5 (hogere kans op selectie)

**Nieuwe Element Types:**
- **Uitgebreide interface** onderaan dialog
- **Type selectie** met beschrijvingen
- **Suno Format** voor audio-specifieke formatting
- **Alle opties** in één interface

## 🎨 Element Types

| Type | Beschrijving | Gebruik |
|------|-------------|---------|
| **keyword** | Belangrijke woorden voor het thema | Basis vocabulaire |
| **power_phrase** | Krachtige zinnen voor refrein/chorus | Emotionele impact |
| **genre** | Muziekgenre en stijl | Stijlbepaling |
| **bpm** | Beats per minute | Tempo instelling |
| **key** | Muzikale toonsoort | Harmonie |
| **instrument** | Instrumenten en sounds | Klankkleur |
| **effect** | Audio effecten | Productie |
| **verse_starter** | Couplet openers | Structuur |
| **rhyme_word** | Rijmwoorden | Rijmschema |
| **vocal_descriptor** | Vocale stijl beschrijving | Zangstijl |

## 🔧 Geavanceerde Opties

### **Usage Context**
- **any**: Altijd beschikbaar
- **intro**: Alleen voor intro
- **verse**: Alleen voor coupletten  
- **chorus**: Alleen voor refrein
- **bridge**: Alleen voor bridge
- **outro**: Alleen voor outro

### **Weight System**
- **1**: Normale kans
- **2**: Dubbele kans
- **3**: Drievoudige kans
- **4-5**: Zeer hoge kans

### **Suno Format**
Voor Suno.ai optimalisatie:
- **Instrumenten**: `[piano]`, `[guitar]`, `[drums]`
- **Effecten**: `[reverb]`, `[chorus]`, `[distortion]`
- **Stijlen**: `[upbeat]`, `[emotional]`, `[energetic]`

## 📊 Real-time Updates

- **Automatische refresh** na elke wijziging
- **Toast notifications** voor feedback
- **Error handling** met duidelijke berichten
- **Loading states** tijdens API calls

## 🎵 Impact op Songtekst Generatie

Alle wijzigingen worden **direct gebruikt** bij nieuwe songtekst generatie:

```javascript
// Voor thema "Verjaardag" na jouw bewerking:
Generated Elements:
- Keywords: ['feestelijk', 'vrolijk', 'jarig'] // Jouw toegevoegde keywords
- Power Phrases: ['Jouw speciale dag is hier'] // Jouw aangepaste phrases
- Instruments: ['[party drums]', '[celebration horns]'] // Jouw instrumenten
```

## 🚀 Workflow Tips

### **Snelle Bewerking**
1. **Bekijk** → **Bewerken** → **Inline wijzigen** → **Enter**
2. Gebruik **Tab** om snel tussen velden te navigeren
3. **Escape** annuleert altijd de huidige bewerking

### **Bulk Toevoegen**
1. **Nieuw Element** sectie onderaan
2. **Type selecteren** → **Content typen** → **Toevoegen**
3. **Form reset** automatisch na toevoegen

### **Optimalisatie**
- **Hoge weight** voor belangrijke elementen
- **Specifieke context** voor gerichte gebruik
- **Suno format** voor muziekproductie

## 🛠️ Technische Details

### **API Endpoints**
```javascript
POST /api/admin/elements          // Nieuw element
PUT /api/admin/elements/{id}      // Element bijwerken  
DELETE /api/admin/elements/{id}   // Element verwijderen
```

### **Real-time Synchronisatie**
- **Optimistische updates** voor snelle UX
- **Error recovery** bij API failures
- **Automatic refresh** na succesvolle wijzigingen

## 🎯 Wat Volgt?

- **Drag & Drop** voor element sortering
- **Bulk operations** (selecteer meerdere elementen)
- **A/B testing** voor element effectiviteit
- **Import/Export** functionaliteit
- **Version control** voor wijzigingsgeschiedenis

## 💡 Pro Tips

1. **Test je wijzigingen** direct door een songtekst te genereren
2. **Gebruik specifieke context** voor betere targeting
3. **Balanceer weight** om variatie te behouden
4. **Suno format** is optioneel maar krachtig
5. **Backup belangrijke elementen** voor je grote wijzigingen maakt

---

**🎵 Happy Editing! Je kunt nu je thema datasets volledig naar eigen wens aanpassen.** 