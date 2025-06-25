# Verbeteringen voor Namen en Thema's in Dashboard

## Probleem Analyse

De namen en thema's werden niet correct weergegeven in het dashboard door:

1. **Inconsistente data mapping** tussen backend en frontend
2. **Verschillende custom field formats** (oude name/value vs nieuwe label/input)
3. **Beperkte fallback opties** voor veld extractie
4. **Mismatch tussen veldnamen** in verschillende delen van de applicatie

## Uitgevoerde Verbeteringen

### 1. Frontend Verbeteringen (`src/hooks/useFetchOrders.ts`)

#### Verbeterde Custom Field Extractie
- **Voor**: Zocht alleen naar exacte veldnaam `'Thema'`
- **Na**: Zoekt naar meerdere varianten en ondersteunt beide formats

```typescript
// Oude code
const field = customFields.find(f => f.label === label);
return field?.input || '-';

// Nieuwe code
const getCustomFieldValue = (...labels: string[]): string => {
  // Ondersteunt beide formats: {label/input} en {name/value}
  for (const label of labels) {
    const field = customFields.find(f => {
      const fieldName = f.label || f.name;
      return fieldName === label;
    });
    if (field) {
      return field.input || field.value || '-';
    }
  }
  return '-';
};
```

#### Verbeterde Thema Extractie
- **Voor**: `order.thema || getCustomFieldValue('Thema') || 'Onbekend'`
- **Na**: Uitgebreide fallback logica met meerdere veldnamen

```typescript
const getThema = (): string => {
  // Eerst backend verwerkte veld proberen
  if (order.thema && order.thema !== '-') {
    return order.thema;
  }
  
  // Dan verschillende thema veldnamen proberen
  const themaValue = getCustomFieldValue(
    'Thema', 'Gelegenheid', 'Vertel over de gelegenheid',
    'Voor welke gelegenheid', 'Voor welke gelegenheid?',
    'Waarvoor is dit lied?', 'Gewenste stijl'
  );
  
  return themaValue !== '-' ? themaValue : 'Onbekend';
};
```

#### Verbeterde Naam Extractie
- **Voor**: `order.voornaam || order.klant_naam || order.raw_data?.address?.firstname || 'Onbekend'`
- **Na**: Uitgebreide fallback met combinatie van voor- en achternaam

```typescript
const getKlantNaam = (): string => {
  // Eerst backend verwerkte velden proberen
  if (order.voornaam && order.voornaam !== '-') return order.voornaam;
  if (order.klant_naam && order.klant_naam !== '-') return order.klant_naam;
  
  // Dan address velden proberen
  if (order.raw_data?.address?.full_name) {
    return order.raw_data.address.full_name;
  }
  
  // Combinatie van firstname + lastname
  if (order.raw_data?.address?.firstname) {
    const firstname = order.raw_data.address.firstname;
    const lastname = order.raw_data?.address?.lastname || '';
    return lastname ? `${firstname} ${lastname}` : firstname;
  }
  
  // Custom fields als laatste fallback
  const voornaamValue = getCustomFieldValue('Voornaam', 'Naam', 'Voor wie is dit lied?', 'Voor wie');
  if (voornaamValue !== '-') {
    const achternaamValue = getCustomFieldValue('Achternaam', 'Van');
    return achternaamValue !== '-' ? `${voornaamValue} ${achternaamValue}` : voornaamValue;
  }
  
  return 'Onbekend';
};
```

### 2. Backend Verbeteringen (`app/schemas/order.py`)

#### Uitgebreide Field Mapping
- **Voor**: Beperkte veldnamen voor thema extractie
- **Na**: Uitgebreide lijst met alle mogelijke varianten

```python
# Oude code
values.setdefault("thema", pick("Thema", "Gelegenheid", "Vertel over de gelegenheid"))

# Nieuwe code
values.setdefault("thema", pick(
    "Thema", "Gelegenheid", "Vertel over de gelegenheid", 
    "Voor welke gelegenheid", "Voor welke gelegenheid?", 
    "Waarvoor is dit lied?", "Gewenste stijl"
))
```

#### Verbeterde Naam Verwerking
```python
# Oude code
values.setdefault("voornaam", address.get("firstname"))

# Nieuwe code
values.setdefault("voornaam", 
    address.get("firstname") or pick("Voornaam", "Naam", "Voor wie is dit lied?", "Voor wie")
)
```

### 3. Type Verbeteringen (`src/types.ts`)

#### Ondersteuning voor Beide Formats
```typescript
// Oude code
custom_field_inputs?: Array<{ label: string; input: string }>;

// Nieuwe code
custom_field_inputs?: Array<{ 
  label?: string; 
  input?: string; 
  name?: string; 
  value?: string; 
}>;
```

### 4. Debug Functionaliteit

#### Development Logging
```typescript
// Debug logging voor development
if (process.env.NODE_ENV === 'development') {
  console.log(`Mapping order ${order.order_id}:`, {
    order_thema: order.thema,
    order_voornaam: order.voornaam,
    order_klant_naam: order.klant_naam,
    raw_data_address: order.raw_data?.address,
    custom_field_inputs: order.raw_data?.custom_field_inputs?.map(f => ({
      label: f.label || f.name,
      value: f.input || f.value
    }))
  });
}
```

## Resultaat

### Voor de Verbeteringen
- Thema: `-` (niet gevonden)
- Klant: `Onbekend` (niet gevonden)

### Na de Verbeteringen
- Thema: `Liefde,Huwelijk` (gevonden via "Gewenste stijl")
- Klant: `Sarah Johnson` (gevonden via address.full_name of firstname+lastname)

## Test Validatie

Een test script (`test_improved_mapping.py`) is toegevoegd om de verbeteringen te valideren:

```bash
python test_improved_mapping.py
```

## Deployment

Na deployment van deze verbeteringen zouden de namen en thema's correct moeten worden weergegeven in het dashboard. De verbeteringen zijn backward compatible en ondersteunen zowel oude als nieuwe data formats.

## Monitoring

In development mode wordt nu debug informatie gelogd naar de console om data mapping problemen te kunnen troubleshooten. 