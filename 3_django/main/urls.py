from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'breeds', views.BreedViewSet)
router.register(r'dogs', views.DogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
