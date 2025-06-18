from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import get_subtitles, extract_video_id

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Subtitles API is running'})

@api_view(['POST'])
def test_video_id(request):
    """Endpoint de debug para probar extracción de ID"""
    video_url = request.data.get('url')
    video_id = extract_video_id(video_url) if video_url else None
    return Response({
        'url': video_url,
        'extracted_id': video_id
    })

@api_view(['POST'])
def get_subtitles_view(request):
    video_url = request.data.get('url')
    
    if not video_url:
        return Response(
            {'error': 'URL is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Llamar al servicio
    result = get_subtitles(video_url)
    
    # Si hay error, devolver 400
    if 'error' in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(result)