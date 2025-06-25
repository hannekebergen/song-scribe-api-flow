"""
Test script om de API te testen en klantnaam extractie te controleren
Simuleert curl commands maar dan via Python
"""

import requests
import json
import os

# Environment variabelen (normaal in .env file)
os.environ['API_KEY'] = 'jouwsong2025'
os.environ['DATABASE_URL'] = 'postgresql://song_scribe_db_user:EHoXvsQYuo72p2mKNhcrbJZYmVOBzw8D@dpg-d10nt6i4d50c73b0doq0-a/song_scribe_db'
os.environ['PLUGPAY_API_KEY'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2U2YmI3ZjA5Zjk5OTczM2U1ODI0MDVmYzc4MDU3M2FjN2E1MDRmMzkwYTlmMmI1Mzg4OGZjMzRiMzlmOTk4MjRmNDIyYzIxYjQzNDJlOWYiLCJpYXQiOjE3NDkwNDU4MzkuMjc4NDE2LCJuYmYiOjE3NDkwNDU4MzkuMjc4NDE3LCJleHAiOjQ5MDQ3MTk0MzkuMjY0MDA0LCJzdWIiOiI2MjcyNSIsInNjb3BlcyI6W119.ehEbbZqXNRLLxoY3EDPop8ZESuWm1jtUmeEZvsX0TuVzZJNeczOD14mSWay1p7sDcKdMcfYV9VO9ORY28P5rROX0PgOT1bcvzbjy5rxVPnv-KwLR-atKu0zX634ebcvolOMfZQVOmO_hRXCmrkXUPUCLvx9DpZyOH8C6xAFL44VpClUhKa9ngtUdCCbnAfh5M411NFcGHDjJprF3k398ISMKLvEyLqYJ7Bx7BuNMcxm7XO00vh1ZzogAD1rhmKM9koprTdFllcKdyetin5Pp-K_2Hics6JpuOWq902hvJPbjEMChwvFX_SeHFXqE10Uk5pLveEm1j6HLhy5tqWn_z5yz8i5Pasxcgk6-bAZBAnnc6vu5gDQG0NC78XxN96q0_hdzn_9f3hlk9KaZsP8Jjf5fYxl2vyPQT_xbQNZwWD0yjdo6Gk0QZfKUFaXhObxtHdpqBLYVHCxHHj9yOcCxyrfpR7HkuTTBEwqq4HyQ3wu5oBJ-JHa9pXSh4n9SIUQh344FeiS0E9Vg12hIqqrtKb6hUEHFDgw4Dbfr0XDOEacZIPigUO6v2iMkOILDrqxLWbXtfC9bpqlcotd0D3t8TKZE8LFqU-EPPRmJTtz3JopDN53zNtiJSRUzKw7MbZJzfoVvNbschrVu-wh2HmeC7ZxUqqoEnsFB4eF70g1RU9I'
os.environ['PLUGPAY_SECRET'] = 'plugpay_webhook_secret_2025'

def test_vercel_frontend():
    """Test de Vercel frontend om te zien of die bereikbaar is"""
    
    print("🌐 Testing Vercel Frontend")
    print("=" * 30)
    
    frontend_url = "https://song-scribe-api-flow.vercel.app"
    
    try:
        response = requests.get(frontend_url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Frontend is online!")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            # Check if it's a React app
            if 'text/html' in response.headers.get('content-type', ''):
                content = response.text
                if 'react' in content.lower() or 'vite' in content.lower():
                    print(f"   📱 React/Vite app detected")
                
                # Check for API configuration in the HTML
                if 'song-scribe-api-flow.onrender.com' in content:
                    print(f"   🔗 Found Render.com API reference in frontend")
                elif 'api' in content.lower():
                    print(f"   🔗 Found API references in frontend")
            
            return True
        else:
            print(f"   ❌ Frontend not accessible: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout accessing frontend")
    except requests.exceptions.ConnectionError:
        print(f"   🔌 Connection error accessing frontend")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return False

def test_local_api():
    """Test de lokale API"""
    
    print("🏠 Testing Local API")
    print("=" * 30)
    
    # Test lokale server
    local_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    headers = {
        "X-API-Key": "jouwsong2025",
        "Content-Type": "application/json"
    }
    
    for base_url in local_urls:
        print(f"\n📡 Testing local server: {base_url}")
        
        # Test health check
        try:
            response = requests.get(f"{base_url}/healthz", timeout=5)
            print(f"   Health check: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Local server is running!")
                
                # Test orders endpoint
                orders_response = requests.get(f"{base_url}/orders/orders", headers=headers, timeout=10)
                print(f"   Orders endpoint: {orders_response.status_code}")
                
                if orders_response.status_code == 200:
                    orders = orders_response.json()
                    print(f"   ✅ Found {len(orders)} orders")
                    return base_url, orders
                else:
                    print(f"   Response: {orders_response.text[:200]}")
                    
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Not running on {base_url}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None, None

def test_api_health():
    """Test of de API server überhaupt draait"""
    
    print("🏥 Testing API Health")
    print("=" * 30)
    
    # Test verschillende mogelijke API URLs
    api_urls = [
        "https://song-scribe-api-flow.onrender.com",  # Render.com (huidige config)
        "https://jouwsong-api.onrender.com",          # Alternatieve Render URL (uit README)
        "https://song-scribe-api-flow.vercel.app/api" # Mogelijk Vercel API route
    ]
    
    # Test health check endpoints
    health_endpoints = [
        "/healthz",
        "/",
        "/health",
        "/api/health"
    ]
    
    for base_url in api_urls:
        print(f"\n🌐 Testing API base: {base_url}")
        
        for endpoint in health_endpoints:
            url = f"{base_url}{endpoint}"
            
            try:
                response = requests.get(url, timeout=10)
                print(f"   {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Server is running at {base_url}!")
                    try:
                        data = response.json()
                        print(f"   Response: {data}")
                    except:
                        print(f"   Response: {response.text[:100]}")
                    return base_url
                elif response.status_code != 404:
                    print(f"   Response: {response.text[:100]}")
                    
            except requests.exceptions.Timeout:
                print(f"   {endpoint}: ⏱️  Timeout")
            except requests.exceptions.ConnectionError:
                print(f"   {endpoint}: 🔌 Connection Error")
            except Exception as e:
                print(f"   {endpoint}: ❌ Error: {e}")
    
    return None

def test_api_endpoints():
    """Test verschillende API endpoints om te zien welke werken"""
    
    print("\n🔍 Testing API Endpoints")
    print("=" * 30)
    
    # Probeer verschillende base URLs
    base_urls = [
        "https://song-scribe-api-flow.onrender.com",
        "https://jouwsong-api.onrender.com",
        "https://song-scribe-api-flow.vercel.app"
    ]
    
    headers = {
        "X-API-Key": "jouwsong2025",
        "Content-Type": "application/json"
    }
    
    # Verschillende endpoints om te proberen (gebaseerd op main.py routing)
    endpoints = [
        "/orders/orders",        # orders router mounted on /orders
        "/orders/orders/orders", # nested route
        "/orders",              # base orders route
        "/api/orders",          # alternative path
        "/api/orders/orders",   # API prefix variant
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing base URL: {base_url}")
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            
            try:
                response = requests.get(url, headers=headers, timeout=20)
                print(f"   {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   ✅ SUCCESS: {len(data)} orders found at {url}")
                            return url, data  # Return successful endpoint and data
                        else:
                            print(f"   ⚠️  Unexpected format: {type(data)}")
                    except:
                        print(f"   ❌ Invalid JSON response")
                elif response.status_code == 401:
                    print(f"   ❌ Unauthorized (check API key)")
                elif response.status_code == 403:
                    print(f"   ❌ Forbidden")
                elif response.status_code == 500:
                    print(f"   ❌ Server Error")
                    print(f"   Error details: {response.text[:200]}")
                elif response.status_code != 404:
                    print(f"   Response: {response.text[:200]}")
                    
            except requests.exceptions.Timeout:
                print(f"   {endpoint}: ⏱️  Timeout (20s)")
            except requests.exceptions.ConnectionError:
                print(f"   {endpoint}: 🔌 Connection Error")
            except Exception as e:
                print(f"   {endpoint}: ❌ Error: {e}")
    
    return None, None

def analyze_klantnaam_data(orders, source_name):
    """Analyseer klantnaam data uit orders"""
    
    print(f"\n🔍 Klantnaam Analysis from {source_name} (First 3 Orders):")
    print("-" * 50)
    
    for i, order in enumerate(orders[:3]):
        order_id = order.get('order_id', 'Unknown')
        print(f"\n📋 Order #{order_id} ({i+1}/3):")
        
        # Backend verwerkte velden
        klant_naam = order.get('klant_naam')
        voornaam = order.get('voornaam')
        
        print(f"  🏷️  Backend klant_naam: {repr(klant_naam)}")
        print(f"  👤 Backend voornaam: {repr(voornaam)}")
        
        # Raw data analyse
        raw_data = order.get('raw_data', {})
        
        # Address data
        address = raw_data.get('address', {})
        if address:
            print(f"  🏠 Address data:")
            print(f"     full_name: {repr(address.get('full_name'))}")
            print(f"     firstname: {repr(address.get('firstname'))}")
            print(f"     lastname: {repr(address.get('lastname'))}")
        
        # Customer data
        customer = raw_data.get('customer', {})
        if customer:
            print(f"  👥 Customer data:")
            print(f"     name: {repr(customer.get('name'))}")
            print(f"     email: {repr(customer.get('email'))}")
        
        # Custom fields (products)
        products = raw_data.get('products', [])
        custom_fields_found = []
        
        for product in products:
            if product.get('custom_field_inputs'):
                for field in product['custom_field_inputs']:
                    label = field.get('label', '')
                    input_val = field.get('input', '')
                    if label and input_val:
                        custom_fields_found.append(f"{label}: {input_val}")
        
        if custom_fields_found:
            print(f"  📝 Custom fields (products):")
            for field in custom_fields_found[:3]:  # Show max 3
                print(f"     {field}")
            if len(custom_fields_found) > 3:
                print(f"     ... and {len(custom_fields_found) - 3} more")
        
        # Root level custom fields (fallback)
        root_custom = raw_data.get('custom_field_inputs', [])
        if root_custom:
            print(f"  📝 Custom fields (root level): {len(root_custom)} fields")
        
        # Simuleer frontend extractie
        def simulate_frontend_extraction():
            # Stap 1: Backend velden
            if voornaam and voornaam not in ['-', 'null', None] and voornaam.strip():
                return voornaam, "backend voornaam"
            
            if klant_naam and klant_naam not in ['-', 'null', None] and klant_naam.strip():
                return klant_naam, "backend klant_naam"
            
            # Stap 2: Address
            if address.get('full_name'):
                return address['full_name'], "address.full_name"
            
            if address.get('firstname'):
                firstname = address['firstname']
                lastname = address.get('lastname', '')
                full = f"{firstname} {lastname}".strip() if lastname else firstname
                return full, "address.firstname+lastname"
            
            # Stap 3: Customer
            if customer.get('name'):
                return customer['name'], "customer.name"
            
            # Stap 4: Custom fields
            name_fields = ['Voornaam', 'Voor wie is dit lied?', 'Voor wie', 'Naam']
            for field in custom_fields_found:
                for name_field in name_fields:
                    if field.startswith(f"{name_field}:"):
                        return field.split(':', 1)[1].strip(), f"custom_field.{name_field}"
            
            return "Onbekend", "fallback"
        
        result_name, source = simulate_frontend_extraction()
        
        print(f"  🎯 Frontend Result: '{result_name}' (via {source})")
        
        # Status check
        if result_name == "Onbekend":
            print(f"  ⚠️  STATUS: PROBLEEM - Geen naam gevonden!")
        else:
            print(f"  ✅ STATUS: OK - Naam succesvol geëxtraheerd")
    
    # Statistieken
    print(f"\n📈 Overall Statistics:")
    print(f"   Total orders: {len(orders)}")
    
    successful_extractions = 0
    backend_success = 0
    address_success = 0
    custom_success = 0
    
    for order in orders[:10]:  # Check first 10
        found_name = False
        
        # Check backend fields
        if order.get('klant_naam') and order.get('klant_naam') not in ['-', 'null', None]:
            backend_success += 1
            found_name = True
        elif order.get('voornaam') and order.get('voornaam') not in ['-', 'null', None]:
            backend_success += 1
            found_name = True
        
        # Check address fields
        elif order.get('raw_data', {}).get('address', {}).get('full_name'):
            address_success += 1
            found_name = True
        elif order.get('raw_data', {}).get('address', {}).get('firstname'):
            address_success += 1
            found_name = True
        
        # Check custom fields
        elif order.get('raw_data', {}).get('products'):
            for product in order['raw_data']['products']:
                if product.get('custom_field_inputs'):
                    for field in product['custom_field_inputs']:
                        if field.get('label') in ['Voornaam', 'Voor wie is dit lied?', 'Voor wie', 'Naam']:
                            custom_success += 1
                            found_name = True
                            break
                if found_name:
                    break
        
        if found_name:
            successful_extractions += 1
    
    total_checked = min(10, len(orders))
    success_rate = (successful_extractions / total_checked) * 100 if total_checked > 0 else 0
    
    print(f"   Success rate (first {total_checked}): {successful_extractions}/{total_checked} ({success_rate:.1f}%)")
    print(f"   - Backend fields: {backend_success}")
    print(f"   - Address fields: {address_success}")  
    print(f"   - Custom fields: {custom_success}")
    
    if success_rate >= 80:
        print(f"   🎉 EXCELLENT: High success rate!")
    elif success_rate >= 60:
        print(f"   ✅ GOOD: Decent success rate")
    else:
        print(f"   ⚠️  NEEDS IMPROVEMENT: Low success rate")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if backend_success < total_checked / 2:
        print(f"   - Run database update script: python update_existing_orders.py")
    if address_success > backend_success:
        print(f"   - Backend extraction is working but needs database update")
    if custom_success > 0:
        print(f"   - Custom field extraction is working as fallback")

def test_api_klantnaam():
    """Test de API om klantnaam extractie te controleren"""
    
    print("🔍 Testing API Klantnaam Extractie")
    print("=" * 50)
    
    # Eerst testen of Vercel frontend werkt
    print("📱 Step 1: Testing Vercel Frontend")
    vercel_online = test_vercel_frontend()
    
    if vercel_online:
        print("   ✅ Frontend is accessible")
    else:
        print("   ⚠️  Frontend issues detected")
    
    # Dan proberen lokale server
    print("\n📱 Step 2: Testing Local API")  
    local_url, local_orders = test_local_api()
    
    if local_url and local_orders:
        print(f"\n✅ Using local server: {local_url}")
        print(f"📊 Total orders: {len(local_orders)}")
        
        if len(local_orders) > 0:
            analyze_klantnaam_data(local_orders, "Local API")
            return
        else:
            print("⚠️  No orders found in local database")
    
    # Anders proberen remote servers
    print("\n📱 Step 3: Testing Remote APIs")
    
    # Eerst testen welke servers draaien
    working_base_url = test_api_health()
    
    if not working_base_url:
        print("\n❌ No API servers appear to be running!")
        print("\n🔧 Possible issues:")
        print("   1. Render.com cold start (can take 30+ seconds)")
        print("   2. Server deployment failed")
        print("   3. Database connection issues")
        print("   4. Environment variables missing on server")
        print("   5. CORS configuration issues")
        print("\n💡 Solutions to try:")
        print("   1. Wait 1-2 minutes and run again (cold start)")
        print("   2. Check Render.com dashboard and logs")
        print("   3. Try starting local server: python main.py")
        print("   4. Check if .env file exists with correct variables")
        return
    
    print(f"\n✅ Found working API server: {working_base_url}")
    
    # Dan zoeken naar werkend orders endpoint
    working_url, orders = test_api_endpoints()
    
    if not working_url:
        print(f"\n❌ API server is running but no working orders endpoint found!")
        print(f"\n🔧 The server at {working_base_url} is responding but:")
        print("   1. Orders endpoints are not configured correctly")
        print("   2. Database migration issues")
        print("   3. API key authentication problems")
        print("   4. Router mounting issues in FastAPI")
        print("\n💡 Check the server logs for more details")
        return
    
    print(f"\n✅ Using working endpoint: {working_url}")
    print(f"📊 Total orders: {len(orders)}")
    
    if len(orders) == 0:
        print("⚠️  No orders found in database")
        print("💡 Try running: POST /orders/fetch to fetch orders from Plug&Pay")
        print("💡 Or check if database is properly connected and migrated")
        return
    
    analyze_klantnaam_data(orders, "Remote API")

if __name__ == "__main__":
    test_api_klantnaam() 