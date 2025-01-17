from rest_framework import serializers

from .models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    """
    Standard serializer for Breed model.
    """
    class Meta:
        model = Breed
        fields = [
            'id', 'name', 'size', 'friendliness',
            'trainability', 'shedding_amount', 'exercise_needs'
        ]


class BreedListSerializer(BreedSerializer):
    """
    Modified serializer for Breed model - List View.
    """
    dog_count = serializers.IntegerField(read_only=True)

    class Meta(BreedSerializer.Meta):
        fields = BreedSerializer.Meta.fields + ['dog_count']


class DogSerializer(serializers.ModelSerializer):
    """
    Standard serializer for Dog model.
    """
    class Meta:
        model = Dog
        fields = [
            'id', 'name', 'age', 'breed', 'gender', 'color',
            'favorite_food', 'favorite_toy'
        ]


class DogListSerializer(DogSerializer):
    """
    Modified serializer for Dog model - List View.
    """
    avg_age = serializers.FloatField(read_only=True)

    class Meta(DogSerializer.Meta):
        fields = DogSerializer.Meta.fields + ['avg_age']


class DogDetailSerializer(DogSerializer):
    """
    Modified serializer for Dog model - Detail View.
    """
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta(DogSerializer.Meta):
        fields = DogSerializer.Meta.fields + ['same_breed_count']
