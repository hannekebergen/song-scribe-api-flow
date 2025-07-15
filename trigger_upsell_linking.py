#!/usr/bin/env python3
"""
Script to manually trigger upsell linking process
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def wait_for_deployment():
    """Wait for deployment to complete"""
    print("⏳ Wachten op deployment...")
    
    # Check if the backend is up
    api_url = 'https://jouwsong-api.onrender.com'
    
    for i in range(10):
        try:
            response = requests.get(f'{api_url}/')
            if response.status_code == 200:
                print("✅ Backend is online")
                return True
        except requests.RequestException:
            pass
        
        print(f"   Poging {i+1}/10...")
        time.sleep(30)  # Wait 30 seconds between attempts
    
    print("❌ Backend niet bereikbaar na 5 minuten")
    return False

def trigger_upsell_linking():
    """Trigger the upsell linking process"""
    api_url = 'https://jouwsong-api.onrender.com/orders/link-upsell-orders'
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print("❌ API_KEY niet gevonden in .env file")
        return False
    
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    print('🔗 Upsell linking proces starten...')
    
    try:
        response = requests.post(api_url, headers=headers, timeout=60)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Linking succesvol!')
            print(f'Message: {data.get("message", "Geen message")}')
            print(f'Updated count: {data.get("updated_count", 0)}')
            print(f'Total processed: {data.get("total_processed", 0)}')
            return True
        else:
            print(f'❌ Fout: {response.text}')
            return False
    
    except requests.Timeout:
        print('❌ Timeout - het proces duurt te lang')
        return False
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

def main():
    """Main function"""
    print("🚀 Upsell Linking Script")
    print("=" * 50)
    
    # Wait for deployment
    if not wait_for_deployment():
        return
    
    # Trigger linking
    if trigger_upsell_linking():
        print("\n✅ Upsell linking proces voltooid!")
        print("Nu kan je de frontend proberen voor order 13275510")
    else:
        print("\n❌ Upsell linking proces mislukt!")

if __name__ == "__main__":
    main() 