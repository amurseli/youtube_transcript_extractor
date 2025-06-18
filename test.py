import requests
import json

# Tu token de API
api_token = "awnenovd2wulr7t6x8t5cavsdaror4lkdgwg4s1b"
headers = {"Authorization": f"Token {api_token}"}

print("🔍 Probando API de Webshare...")
print("=" * 50)

# 1. Obtener perfil
print("\n1. PERFIL DE USUARIO:")
try:
    response = requests.get(
        "https://proxy.webshare.io/api/v2/profile/",
        headers=headers
    )
    if response.status_code == 200:
        profile = response.json()
        print(f"✓ Email: {profile.get('email', 'N/A')}")
        print(f"✓ Tipo de cuenta: {profile.get('subscription_plan', {}).get('name', 'N/A')}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 2. Obtener lista de proxies
print("\n2. LISTA DE PROXIES:")
try:
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/list/",
        headers=headers,
        params={"mode": "direct", "page_size": 25}
    )
    if response.status_code == 200:
        data = response.json()
        proxies = data.get('results', [])
        print(f"✓ Total de proxies: {data.get('count', 0)}")
        
        if proxies:
            print("\nPrimeros 3 proxies:")
            for i, proxy in enumerate(proxies[:3], 1):
                print(f"\nProxy {i}:")
                print(f"  - IP: {proxy.get('proxy_address')}:{proxy.get('port')}")
                print(f"  - Username: {proxy.get('username')}")
                print(f"  - Password: {proxy.get('password')}")
                print(f"  - Tipo: {proxy.get('country_code', 'N/A')}")
                
                # Guardar para test
                if i == 1:
                    test_proxy = proxy
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 3. Probar un proxy
if 'test_proxy' in locals():
    print("\n3. PROBANDO PROXY:")
    proxy_url = f"http://{test_proxy['username']}:{test_proxy['password']}@{test_proxy['proxy_address']}:{test_proxy['port']}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        print(f"✓ Proxy funciona! IP: {response.json()['origin']}")
    except Exception as e:
        print(f"✗ Error al usar proxy: {e}")

print("\n" + "=" * 50)
print("Revisa los datos de username/password de los proxies arriba")