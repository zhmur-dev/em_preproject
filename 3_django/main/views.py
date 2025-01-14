from rest_framework import permissions, viewsets

from .models import Breed, Dog
from .serializers import BreedSerializer, DogSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    queryset = Breed.objects.all().order_by('-id')
    serializer_class = BreedSerializer
    permission_classes = [permissions.AllowAny]


class DogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dogs to be viewed or edited.
    """
    queryset = Dog.objects.all().order_by('-id')
    serializer_class = DogSerializer
    permission_classes = [permissions.AllowAny]
