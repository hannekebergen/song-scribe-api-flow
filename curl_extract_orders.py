#!/usr/bin/env python3
"""
Eenvoudige curl-gebaseerde versie om orders op te halen en te verwerken.
"""

import subprocess
import json
import os
from datetime import datetime

# Configuratie
API_KEY = "jouwsong2025"
BASE_URL = "https://jouwsong-api.onrender.com"

def run_curl_command():
    """
    Voert curl command uit om orders op te halen.
    """
    url = f"{BASE_URL}/orders/orders"
    
    curl_command = [
        "curl",
        "-X", "GET",
        "-H", f"X-API-Key: {API_KEY}",
        "-H", "Content-Type: application/json",
        url
    ]
    
    print(f"🔄 Uitvoeren van curl command...")
    print(" ".join(curl_command))
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Curl succesvol uitgevoerd")
            return json.loads(result.stdout)
        else:
            print(f"❌ Curl fout: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Curl timeout")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse fout: {e}")
        print(f"Response: {result.stdout}")
        return None
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return None

def main():
    """
    Hoofdfunctie.
    """
    print("🎵 Curl-based Orders Extractor")
    print("=" * 40)
    
    # Voer curl uit
    orders = run_curl_command()
    
    if orders:
        print(f"✅ {len(orders)} orders opgehaald")
        
        # Sla ruwe data op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"orders_raw_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 Ruwe orders opgeslagen in: {filename}")
        
        # Laat eerste order zien als voorbeeld
        if orders:
            print(f"\n🔍 Eerste order voorbeeld:")
            first_order = orders[0]
            print(f"   • Order ID: {first_order.get('order_id', 'N/A')}")
            print(f"   • Klant: {first_order.get('klant_naam', 'N/A')}")
            print(f"   • Product: {first_order.get('product_naam', 'N/A')}")
            print(f"   • Thema: {first_order.get('thema', 'N/A')}")
            print(f"   • Beschrijving: {first_order.get('beschrijving', 'N/A')}")
    else:
        print("❌ Geen orders opgehaald")

if __name__ == "__main__":
    main() 