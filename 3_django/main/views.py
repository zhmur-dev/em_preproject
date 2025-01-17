from django.db.models import Avg, Count
from django.db.models.functions import Round
from rest_framework import permissions, viewsets

from .models import Breed, Dog
from .serializers import (
    BreedListSerializer, BreedSerializer,
    DogDetailSerializer, DogListSerializer
)


class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Modified get_queryset() method that returns queryset
        depending on if "List View" or "Detail View" is made use of.
        """
        if self.action == 'list' or self.action == 'post':
            return Breed.objects.annotate(
                dog_count=Count('dogs'),
            ).order_by('-id')
        return Breed.objects.all().order_by('-id')

    def get_serializer_class(self):
        """
        Modified get_serializer_class() method that returns serializer
        depending on if "List View" or "Detail View" is made use of.
        """
        if self.action == 'list' or self.action == 'post':
            return BreedListSerializer
        return BreedSerializer


class DogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dogs to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Modified get_queryset() method that returns queryset
        depending on if "List View" or "Detail View" is made use of.
        """
        if self.action == 'list' or self.action == 'post':
            return Dog.objects.annotate(
                avg_age=Round(Avg('breed__dogs__age'), precision=2)
            ).order_by('-id')
        return Dog.objects.annotate(
            same_breed_count=Count('breed__dogs'),
        ).order_by('-id')

    def get_serializer_class(self):
        """
        Modified get_serializer_class() method that returns serializer
        depending on if "List View" or "Detail View" is made use of.
        """
        if self.action == 'list' or self.action == 'post':
            return DogListSerializer
        return DogDetailSerializer
