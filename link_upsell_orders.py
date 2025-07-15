import requests
import os
from dotenv import load_dotenv

load_dotenv()

def link_upsell_orders():
    """Voer het upsell linking proces uit"""
    api_url = 'https://jouwsong-api.onrender.com/orders/link-upsell-orders'
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print("❌ API_KEY niet gevonden in .env file")
        return
    
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    print('🔗 Upsell orders linken...')
    
    try:
        response = requests.post(api_url, headers=headers)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Linking succesvol!')
            print(f'Updated orders: {data.get("updated_orders", 0)}')
            print(f'Details: {data.get("details", "Geen details beschikbaar")}')
        else:
            print(f'❌ Fout: {response.text}')
    
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    link_upsell_orders() 