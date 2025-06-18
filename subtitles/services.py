from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    YouTubeRequestFailed
)
import re
import os
import random
import time

def extract_video_id(url):
    """
    Extrae el ID del video de una URL de YouTube
    Soporta: youtube.com/watch?v=ID y youtu.be/ID
    """
    # Patrón para youtube.com/watch?v=VIDEO_ID
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if match:
        return match.group(1)
    return None

def get_all_proxies():
    """
    Obtiene todos los proxies disponibles
    """
    proxy_list = os.getenv('WEBSHARE_PROXY_LIST', '')
    if not proxy_list:
        return []
    
    return [p.strip() for p in proxy_list.split(',') if p.strip()]

def get_proxy_config(exclude_proxies=None):
    """
    Construye la configuración del proxy desde las variables de entorno
    Permite excluir proxies que ya fallaron
    """
    if os.getenv('USE_PROXY', 'False') != 'True':
        return None
    
    username = os.getenv('WEBSHARE_PROXY_USERNAME')
    password = os.getenv('WEBSHARE_PROXY_PASSWORD')
    
    if not all([username, password]):
        print("Warning: Proxy enabled but credentials incomplete")
        return None
    
    # Obtener proxies disponibles
    all_proxies = get_all_proxies()
    if not all_proxies:
        print("Warning: No proxies found in WEBSHARE_PROXY_LIST")
        return None
    
    # Filtrar proxies excluidos
    if exclude_proxies:
        available_proxies = [p for p in all_proxies if p not in exclude_proxies]
    else:
        available_proxies = all_proxies
    
    if not available_proxies:
        print("Warning: All proxies have been excluded")
        return None
    
    # Seleccionar un proxy al azar
    selected_proxy = random.choice(available_proxies)
    print(f"Selected proxy: {selected_proxy}")
    
    proxy_url = f"http://{username}:{password}@{selected_proxy}"
    return {
        "http": proxy_url,
        "https": proxy_url
    }, selected_proxy

def get_subtitles(video_url):
    """
    Obtiene los subtítulos de un video de YouTube con reintentos
    """
    # Extraer ID del video
    video_id = extract_video_id(video_url)
    if not video_id:
        return {'error': 'Invalid YouTube URL'}
    
    # Verificar configuración de proxy
    use_proxy = os.getenv('USE_PROXY', 'False') == 'True'
    print(f"USE_PROXY setting: {os.getenv('USE_PROXY')} -> using proxy: {use_proxy}")
    
    # Lista de proxies que han fallado
    failed_proxies = []
    max_retries = 3 if use_proxy else 1  # Solo 1 intento sin proxy
    
    for attempt in range(max_retries):
        try:
            # Obtener configuración de proxy solo si está habilitado
            if use_proxy:
                proxy_result = get_proxy_config(exclude_proxies=failed_proxies)
                if proxy_result:
                    proxies, current_proxy = proxy_result
                    print(f"Attempt {attempt + 1} with proxy {current_proxy}")
                else:
                    proxies = None
                    current_proxy = None
                    print(f"Attempt {attempt + 1} - No proxy available")
            else:
                proxies = None
                current_proxy = None
                print(f"Attempt {attempt + 1} WITHOUT proxy (direct connection)")
            
            # Obtener transcripción
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
            
            return {
                'video_id': video_id,
                'subtitles': transcript,
                'subtitle_count': len(transcript),
                'proxy_used': bool(proxies),
                'attempts': attempt + 1
            }
            
        except YouTubeRequestFailed as e:
            # Verificar si es un error 429 (Too Many Requests)
            if "429" in str(e) or "Too Many Requests" in str(e):
                print(f"Rate limited on attempt {attempt + 1}")
                if current_proxy:
                    failed_proxies.append(current_proxy)
                    print(f"Marked proxy {current_proxy} as failed")
                
                # Esperar un poco antes de reintentar
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # 2, 4, 6 segundos
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    return {
                        'error': 'Too many failed attempts',
                        'details': str(e),
                        'proxy_used': bool(proxies),
                        'attempts': attempt + 1
                    }
            else:
                # Otro tipo de error de YouTube
                return {
                    'error': f'YouTube request failed: {type(e).__name__}',
                    'details': str(e),
                    'proxy_used': bool(proxies)
                }
                
        except TranscriptsDisabled:
            # Intentar listar transcripciones disponibles para más info
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
                available = []
                for t in transcript_list:
                    available.append({
                        'language': t.language,
                        'language_code': t.language_code,
                        'is_generated': t.is_generated
                    })
                return {
                    'error': 'Could not fetch default transcript',
                    'available_transcripts': available,
                    'suggestion': 'Try specifying a language code'
                }
            except:
                return {'error': 'Subtitles are disabled for this video'}
                
        except NoTranscriptFound:
            return {'error': 'No transcript found for this video'}
        except VideoUnavailable:
            return {'error': 'Video is unavailable'}
        except Exception as e:
            return {
                'error': f'Unexpected error: {type(e).__name__}',
                'details': str(e),
                'proxy_used': bool(proxies)
            }