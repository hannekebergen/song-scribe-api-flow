"""
Script om een API update te triggeren voor bestaande orders
"""

import requests
import json

def trigger_api_update():
    """Trigger API update via POST request"""
    
    api_url = "https://jouwsong-api.onrender.com/orders/fetch"
    headers = {
        "X-API-Key": "jouwsong2025",
        "Content-Type": "application/json"
    }
    
    print(f"🚀 Triggering API update via: {api_url}")
    
    try:
        response = requests.post(api_url, headers=headers, timeout=30)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📊 Response: {json.dumps(data, indent=2)}")
            
            # Check if any orders were processed
            result = data.get('result', {})
            new_orders = result.get('new_orders', 0)
            skipped_orders = result.get('skipped_orders', 0)
            
            print(f"\n📈 Summary:")
            print(f"   New orders: {new_orders}")
            print(f"   Skipped orders: {skipped_orders}")
            print(f"   Total processed: {new_orders + skipped_orders}")
            
            if skipped_orders > 0:
                print(f"\n💡 {skipped_orders} orders were skipped - these might have been updated!")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out (30s)")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    trigger_api_update() 