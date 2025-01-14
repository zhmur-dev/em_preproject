from rest_framework import serializers

from .models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = [
            'id', 'name', 'size', 'friendliness',
            'trainability', 'shedding_amount', 'exercise_needs'
        ]


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            'id', 'name', 'age', 'breed', 'gender', 'color',
            'favorite_food', 'favorite_toy'
        ]
