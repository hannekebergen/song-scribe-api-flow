#!/usr/bin/env python3
"""
Script om alle orders op te halen en gewenste stijlen en beschrijvingen te extraheren.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuratie
API_KEY = "jouwsong2025"
BASE_URL = "https://jouwsong-api.onrender.com"  # Render backend URL

def get_orders_from_api() -> List[Dict[str, Any]]:
    """
    Haalt alle orders op via de API.
    """
    url = f"{BASE_URL}/orders/orders"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🔄 Orders ophalen van {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        orders = response.json()
        print(f"✅ {len(orders)} orders opgehaald")
        return orders
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Fout bij ophalen van orders: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return []

def extract_styles_and_descriptions(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extraheert gewenste stijlen en beschrijvingen uit de orders.
    """
    extracted_data = []
    
    for order in orders:
        order_id = order.get('order_id')
        klant_naam = order.get('klant_naam') or order.get('voornaam', 'Onbekend')
        
        # Extract custom fields from raw_data
        raw_data = order.get('raw_data', {})
        custom_fields = {}
        
        # Probeer custom fields uit products te halen (echte API structuur)
        for product in raw_data.get('products', []):
            for field in product.get('custom_field_inputs', []):
                if isinstance(field, dict):
                    label = field.get('label')
                    value = field.get('input')  # Echte API gebruikt "input"
                    if label and value:
                        custom_fields[label] = value
        
        # Fallback naar root level custom fields
        if not custom_fields:
            for field in raw_data.get('custom_field_inputs', []):
                if isinstance(field, dict):
                    key = field.get('name') or field.get('label')
                    value = field.get('value') or field.get('input')
                    if key and value:
                        custom_fields[key] = value
        
        # Helper functie om custom fields te zoeken
        def pick(*keys):
            return next((custom_fields[k] for k in keys if k in custom_fields), None)
        
        # Extract gewenste stijlen en beschrijvingen
        gewenste_stijl = (
            order.get('thema') or 
            pick("Vertel over de gelegenheid", "Thema", "Gelegenheid", "Voor welke gelegenheid", 
                 "Voor welke gelegenheid?", "Waarvoor is dit lied?", "Gewenste stijl") or
            order.get('toon') or
            pick("Toon", "Sfeer", "Gewenste toon", "Stijl")
        )
        
        beschrijving = (
            order.get('beschrijving') or 
            pick("Beschrijf", "Persoonlijk verhaal", "Vertel iets over deze persoon", 
                 "Toelichting", "Vertel over de persoon", "Vertel over deze persoon", 
                 "Vertel over je wensen", "Vertel over je ideeën", "Vertel je verhaal", 
                 "Vertel meer", "Vertel")
        )
        
        # Structuur info
        structuur = (
            order.get('structuur') or
            pick("Structuur", "Song structuur", "Opbouw")
        )
        
        extracted_item = {
            'order_id': order_id,
            'klant_naam': klant_naam,
            'product_naam': order.get('product_naam'),
            'bestel_datum': order.get('bestel_datum'),
            'gewenste_stijl': gewenste_stijl,
            'beschrijving': beschrijving,
            'structuur': structuur,
            'thema': order.get('thema'),
            'toon': order.get('toon'),
            'deadline': order.get('deadline'),
            'type_order': order.get('typeOrder'),
            'alle_custom_fields': custom_fields  # Voor debugging
        }
        
        extracted_data.append(extracted_item)
    
    return extracted_data

def save_to_json(data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """
    Slaat de data op in een JSON bestand.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"orders_styles_descriptions_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    return filename

def main():
    """
    Hoofdfunctie die alles coördineert.
    """
    print("🎵 Song Scribe - Orders Stijlen & Beschrijvingen Extractor")
    print("=" * 60)
    
    # Haal orders op
    orders = get_orders_from_api()
    if not orders:
        print("❌ Geen orders gevonden of fout bij ophalen")
        return
    
    # Extract stijlen en beschrijvingen
    print(f"🔄 Stijlen en beschrijvingen extraheren uit {len(orders)} orders...")
    extracted_data = extract_styles_and_descriptions(orders)
    
    # Filter orders met interessante data
    orders_with_data = [
        order for order in extracted_data 
        if order.get('gewenste_stijl') or order.get('beschrijving') or order.get('structuur')
    ]
    
    print(f"✅ {len(orders_with_data)} orders hebben stijl/beschrijving data")
    
    # Sla op in JSON
    filename = save_to_json(extracted_data)
    filename_filtered = save_to_json(orders_with_data, f"filtered_{filename}")
    
    # Statistieken
    print("\n📊 Statistieken:")
    print(f"   • Totaal orders: {len(orders)}")
    print(f"   • Orders met stijl/beschrijving: {len(orders_with_data)}")
    print(f"   • Orders met gewenste stijl: {sum(1 for o in extracted_data if o.get('gewenste_stijl'))}")
    print(f"   • Orders met beschrijving: {sum(1 for o in extracted_data if o.get('beschrijving'))}")
    print(f"   • Orders met structuur: {sum(1 for o in extracted_data if o.get('structuur'))}")
    
    print(f"\n💾 Bestanden opgeslagen:")
    print(f"   • Alle orders: {filename}")
    print(f"   • Orders met data: {filename_filtered}")
    
    # Toon voorbeelden
    if orders_with_data:
        print(f"\n🔍 Voorbeeld van eerste order met data:")
        example = orders_with_data[0]
        print(f"   • Order ID: {example['order_id']}")
        print(f"   • Klant: {example['klant_naam']}")
        print(f"   • Gewenste stijl: {example['gewenste_stijl']}")
        print(f"   • Beschrijving: {example['beschrijving'][:100] if example.get('beschrijving') else 'Geen'}...")

if __name__ == "__main__":
    main() 