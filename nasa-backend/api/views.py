import os
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Dataset, Annotation, ImageMetadata, TileCache
from .serializers import DatasetSerializer, AnnotationSerializer, ImageMetadataSerializer, TileCacheSerializer
from .nasa_services import NASADataFetcher

class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for NASA datasets
    GET /api/datasets/ - List all datasets
    GET /api/datasets/{slug}/ - Get specific dataset details
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = "slug"  # Use slug instead of ID in URLs

    @action(detail=True, methods=['get'])
    def info(self, request, slug=None):
        """Custom endpoint: /api/datasets/{slug}/info/"""
        dataset = self.get_object()
        return Response(self.get_serializer(dataset).data)

class AnnotationViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for user annotations
    GET /api/annotations/ - List annotations
    POST /api/annotations/ - Create new annotation
    PUT /api/annotations/{id}/ - Update annotation
    DELETE /api/annotations/{id}/ - Delete annotation
    """
    queryset = Annotation.objects.all().select_related('dataset')
    serializer_class = AnnotationSerializer
    
    def get_queryset(self):
        """Filter annotations by dataset if specified"""
        queryset = super().get_queryset()
        dataset = self.request.query_params.get('dataset')
        if dataset:
            queryset = queryset.filter(dataset__slug=dataset)
        return queryset

class ImageMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for NASA image metadata
    GET /api/metadata/ - List all image metadata
    GET /api/metadata/{id}/ - Get specific metadata
    """
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer
    
    def get_queryset(self):
        """Filter by dataset if specified"""
        queryset = super().get_queryset()
        dataset = self.request.query_params.get('dataset')
        if dataset:
            queryset = queryset.filter(dataset__slug=dataset)
        return queryset

@api_view(['GET'])
def nasa_apod(request):
    """
    Get NASA's Astronomy Picture of the Day
    GET /api/nasa/apod/ - Today's picture
    GET /api/nasa/apod/?date=2023-10-01 - Specific date
    """
    date = request.GET.get('date', None)
    fetcher = NASADataFetcher()
    data = fetcher.fetch_apod(date)
    if data:
        return Response(data)
    return Response({'error': 'Failed to fetch APOD data'}, status=400)

@api_view(['GET'])
def search_features(request):
    """
    Search annotations by feature name
    GET /api/search/?q=crater - Search for "crater" in annotations
    """
    q = request.GET.get('q', '').strip()
    if not q:
        return Response({"results": []})
    
    annotations = Annotation.objects.filter(feature_name__icontains=q)[:50]
    serializer = AnnotationSerializer(annotations, many=True)
    return Response({"results": serializer.data})

def get_tile(request, dataset, z, x, y, ext):
    """
    Serve map tiles for frontend display
    GET /tiles/{dataset}/{z}/{x}/{y}.png - Get specific tile
    """
    # Sanitize dataset slug to prevent directory traversal
    ds_slug = os.path.basename(dataset)
    base_tiles_dir = os.path.join(settings.TILES_ROOT, ds_slug)
    
    tile_path = os.path.join(base_tiles_dir, str(z), str(x), f"{y}.{ext}")
    
    # Try alternative file extension if requested one doesn't exist
    if not os.path.exists(tile_path):
        alt_ext = 'png' if ext.lower() == 'jpg' else 'jpg'
        alt_path = os.path.join(base_tiles_dir, str(z), str(x), f"{y}.{alt_ext}")
        if os.path.exists(alt_path):
            tile_path = alt_path
    
    if os.path.exists(tile_path):
        content_type = "image/png" if tile_path.endswith('.png') else "image/jpeg"
        return FileResponse(open(tile_path, 'rb'), content_type=content_type)
    
    raise Http404("Tile not found")
