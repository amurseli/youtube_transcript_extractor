#!/usr/bin/env python3
"""
Script para probar la conexión del proxy
"""
import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def test_proxy_connection():
    username = os.getenv('WEBSHARE_USERNAME')
    password = os.getenv('WEBSHARE_PASSWORD')
    proxy_list = os.getenv('WEBSHARE_PROXY_LIST', '')
    
    if not proxy_list:
        print("❌ No hay proxies configurados")
        return
    
    proxy = proxy_list.split(',')[0].strip()
    print(f"🔧 Probando proxy: {proxy}")
    print(f"👤 Username: {username}")
    print(f"🔑 Password: {'*' * len(password) if password else 'NO PASSWORD'}")
    
    # Probar diferentes formatos
    formats = [
        # Formato 1: Standard
        {
            "http": f"http://{username}:{password}@{proxy}",
            "https": f"http://{username}:{password}@{proxy}"
        },
        # Formato 2: Con https
        {
            "http": f"http://{username}:{password}@{proxy}",
            "https": f"https://{username}:{password}@{proxy}"
        },
        # Formato 3: Solo HTTP
        {
            "http": f"http://{username}:{password}@{proxy}"
        }
    ]
    
    print("\n📡 Probando conexión básica a internet...")
    for i, proxies in enumerate(formats, 1):
        print(f"\nFormato {i}: {list(proxies.values())[0][:30]}...")
        try:
            # Test básico
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
            print(f"✅ Conexión exitosa! IP: {response.json().get('origin', 'Unknown')}")
            
            # Test con YouTube
            print("🎥 Probando con YouTube...")
            video_id = "dQw4w9WgXcQ"
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
            print(f"✅ YouTube funciona! Subtítulos obtenidos: {len(transcript)} líneas")
            return True
            
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {str(e)[:100]}...")
    
    print("\n🔍 Posibles problemas:")
    print("1. Verifica que el username/password sean correctos")
    print("2. Asegúrate de que los proxies sean 'Residential' no 'Datacenter'")
    print("3. Verifica que tu IP esté en whitelist si es necesario")

if __name__ == "__main__":
    test_proxy_connection()