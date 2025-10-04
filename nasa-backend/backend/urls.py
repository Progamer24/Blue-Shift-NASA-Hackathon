from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from api.views import DatasetViewSet, AnnotationViewSet, ImageMetadataViewSet, get_tile, search_features, nasa_apod

# Create router for REST API endpoints
router = routers.DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'annotations', AnnotationViewSet, basename='annotation')
router.register(r'metadata', ImageMetadataViewSet, basename='metadata')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/search/', search_features, name='search_features'),
    path('api/nasa/apod/', nasa_apod, name='nasa_apod'),
    re_path(r'^tiles/(?P<dataset>[-\w]+)/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)\.(?P<ext>png|jpg)$', 
            get_tile, name='get_tile'),
]
