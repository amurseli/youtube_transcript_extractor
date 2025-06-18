from youtube_transcript_api import YouTubeTranscriptApi

# Credenciales del proxy - probemos con el segundo de tu lista
proxies = {
    "http": "http://ecdumxlq:8w06cb1fkws4@207.244.217.165:6712",
    "https": "http://ecdumxlq:8w06cb1fkws4@207.244.217.165:6712"
}

# Videos de prueba
test_videos = [
    ("dQw4w9WgXcQ", "Rick Roll"),
    ("hY7m5jjJ9mM", "TED Talk"),
    ("kJQP7kiw5Fk", "Luis Fonsi - Despacito"),
]

for video_id, name in test_videos:
    print(f"\n{'='*50}")
    print(f"Probando: {name} ({video_id})")
    print('='*50)
    
    try:
        # Listar transcripciones disponibles
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
        print("Transcripciones disponibles:")
        
        available_langs = []
        for transcript in transcript_list:
            print(f"  - {transcript.language} ({transcript.language_code})")
            print(f"    Auto-generado: {transcript.is_generated}")
            available_langs.append(transcript.language_code)
        
        # Intentar obtener en inglés o español
        for lang in ['en', 'es', available_langs[0] if available_langs else 'en']:
            try:
                print(f"\nIntentando obtener subtítulos en '{lang}'...")
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang], proxies=proxies)
                print(f"✓ Éxito! {len(transcript)} líneas")
                print(f"Primera línea: {transcript[0]['text'][:50]}...")
                break
            except:
                print(f"✗ No disponible en '{lang}'")
                
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)[:1000]}...")