from youtube_transcript_api import YouTubeTranscriptApi

print("Probando SIN proxy...")
try:
    transcript = YouTubeTranscriptApi.get_transcript("dQw4w9WgXcQ")
    print(f"✓ Funciona sin proxy! {len(transcript)} líneas")
except Exception as e:
    print(f"✗ Error sin proxy: {type(e).__name__}: {str(e)[:100]}")