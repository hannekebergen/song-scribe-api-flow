"""
Script om het nieuwe /orders/update-names endpoint te testen
"""

import requests
import json

def test_update_endpoint():
    """Test het nieuwe update-names endpoint"""
    
    api_url = "https://jouwsong-api.onrender.com/orders/update-names"
    headers = {
        "X-API-Key": "jouwsong2025",
        "Content-Type": "application/json"
    }
    
    print(f"🚀 Testing update-names endpoint: {api_url}")
    
    try:
        response = requests.post(api_url, headers=headers, timeout=60)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📊 Response: {json.dumps(data, indent=2)}")
            
            # Extract results
            message = data.get('message', '')
            updated_count = data.get('updated_count', 0)
            total_processed = data.get('total_processed', 0)
            
            print(f"\n📈 Summary:")
            print(f"   Message: {message}")
            print(f"   Updated orders: {updated_count}")
            print(f"   Total processed: {total_processed}")
            
            if updated_count > 0:
                print(f"\n🎉 SUCCESS: {updated_count} orders were updated with improved klantnaam extraction!")
            else:
                print(f"\n⚠️  No orders were updated - they might already have names or lack raw_data")
                
        elif response.status_code == 404:
            print(f"❌ Endpoint not found - the new code hasn't been deployed yet")
            print(f"💡 The server needs to be redeployed with the new endpoint")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out (60s) - the update process might be running")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_update_endpoint() 