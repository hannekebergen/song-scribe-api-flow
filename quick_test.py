import requests
import json

# API Configuration
API_BASE_URL = "https://jouwsong-api.onrender.com"
API_KEY = "jouwsong2025"

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

def quick_test():
    """Quick test to check backend status"""
    print("🔍 Quick Backend Status Check")
    print("=" * 40)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{API_BASE_URL}/api/ai/suno-health", headers=headers)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data.get('status')}")
            print(f"✅ SUNO Key: {data.get('has_suno_key')}")
        else:
            print(f"❌ Health Error: {response.text}")
    except Exception as e:
        print(f"❌ Health Failed: {e}")
    
    # Test 2: Music Generation
    try:
        payload = {
            "customMode": True,
            "instrumental": False,
            "model": "V4_5",
            "style": "pop",
            "title": "Test Song",
            "prompt": "This is a test song",
            "callBackUrl": "https://api.example.com/callback"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/ai/generate-music", headers=headers, json=payload)
        print(f"Music Generation: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Music Success: {data}")
        else:
            print(f"❌ Music Error: {response.text}")
    except Exception as e:
        print(f"❌ Music Failed: {e}")

if __name__ == "__main__":
    quick_test() 