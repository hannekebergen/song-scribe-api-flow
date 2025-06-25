import requests
import json

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2U2YmI3ZjA5Zjk5OTczM2U1ODI0MDVmYzc4MDU3M2FjN2E1MDRmMzkwYTlmMmI1Mzg4OGZjMzRiMzlmOTk4MjRmNDIyYzIxYjQzNDJlOWYiLCJpYXQiOjE3NDkwNDU4MzkuMjc4NDE2LCJuYmYiOjE3NDkwNDU4MzkuMjc4NDE3LCJleHAiOjQ5MDQ3MTk0MzkuMjY0MDA0LCJzdWIiOiI2MjcyNSIsInNjb3BlcyI6W119.ehEbbZqXNRLLxoY3EDPop8ZESuWm1jtUmeEZvsX0TuVzZJNeczOD14mSWay1p7sDcKdMcfYV9VO9ORY28P5rROX0PgOT1bcvzbjy5rxVPnv-KwLR-atKu0zX634ebcvolOMfZQVOmO_hRXCmrkXUPUCLvx9DpZyOH8C6xAFL44VpClUhKa9ngtUdCCbnAfh5M411NFcGHDjJprF3k398ISMKLvEyLqYJ7Bx7BuNMcxm7XO00vh1ZzogAD1rhmKM9koprTdFllcKdyetin5Pp-K_2Hics6JpuOWq902hvJPbjEMChwvFX_SeHFXqE10Uk5pLveEm1j6HLhy5tqWn_z5yz8i5Pasxcgk6-bAZBAnnc6vu5gDQG0NC78XxN96q0_hdzn_9f3hlk9KaZsP8Jjf5fYxl2vyPQT_xbQNZwWD0yjdo6Gk0QZfKUFaXhObxtHdpqBLYVHCxHHj9yOcCxyrfpR7HkuTTBEwqq4HyQ3wu5oBJ-JHa9pXSh4n9SIUQh344FeiS0E9Vg12hIqqrtKb6hUEHFDgw4Dbfr0XDOEacZIPigUO6v2iMkOILDrqxLWbXtfC9bpqlcotd0D3t8TKZE8LFqU-EPPRmJTtz3JopDN53zNtiJSRUzKw7MbZJzfoVvNbschrVu-wh2HmeC7ZxUqqoEnsFB4eF70g1RU9I"

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

print('🔌 Testing Plug&Pay API...')
try:
    response = requests.get('https://api.plugandpay.nl/v1/orders', headers=headers, timeout=30)
    print(f'📡 Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Success! Orders found: {len(data.get("data", []))}')
        
        if data.get('data'):
            first_order = data['data'][0]
            print(f'\n🔍 First order analysis:')
            print(f'  ID: {first_order.get("id")}')
            print(f'  Created: {first_order.get("created_at")}')
            print(f'  Keys: {list(first_order.keys())}')
            
            # Check customer
            if 'customer' in first_order:
                customer = first_order['customer']
                print(f'  Customer: {customer.get("name", "N/A")} ({customer.get("email", "N/A")})')
            
            # Check products
            if 'products' in first_order:
                products = first_order['products']
                print(f'  Products: {len(products)} items')
                for i, product in enumerate(products[:2]):  # Show first 2
                    print(f'    {i+1}. {product.get("title", product.get("name", "N/A"))} (ID: {product.get("id")})')
            
            # Check custom fields
            for field_name in ['custom_field_inputs', 'custom_fields', 'fields']:
                if field_name in first_order:
                    fields = first_order[field_name]
                    print(f'  {field_name}: {len(fields) if isinstance(fields, list) else "dict"}')
                    break
            
            # Save sample
            with open('sample_order.json', 'w', encoding='utf-8') as f:
                json.dump(first_order, f, indent=2, ensure_ascii=False, default=str)
            print(f'💾 Sample order saved to sample_order.json')
            
    else:
        print(f'❌ Error {response.status_code}: {response.text[:200]}')
        
except Exception as e:
    print(f'❌ Exception: {e}') 