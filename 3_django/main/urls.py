from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'breeds', views.BreedViewSet, basename='breed')
router.register(r'dogs', views.DogViewSet, basename='dog')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include(router.urls)),
]
