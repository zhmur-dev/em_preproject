from django.db import models

from .const import BREED_SCALE, BREED_SIZES, CHARFIELD_MAXLENGTH


class BreedScaleField(models.PositiveSmallIntegerField):
    """
    Custom PositiveSmallIntegerField
    to represent a Breed model characteristic scale
    with pre-defined possible values.
    """
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = BREED_SCALE
        kwargs['blank'] = False
        kwargs['null'] = False
        super().__init__(*args, **kwargs)


class Breed(models.Model):
    """
    Represents a dog breed.

    All attributes are mandatory and not nullable.
    Breed name has to be unique.

    Attributes:
        name (str): Unique name of the breed.
        size (str): Possible values defined in BREED_SIZES.
        friendliness (int): Possible values defined in BREED_SCALE.
        trainability (int): Possible values defined in BREED_SCALE.
        shedding_amount (int): Possible values defined in BREED_SCALE.
        exercise_needs (int): Possible values defined in BREED_SCALE.
    """
    name = models.CharField(
        max_length=CHARFIELD_MAXLENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    size = models.CharField(
        max_length=CHARFIELD_MAXLENGTH,
        choices=BREED_SIZES,
        blank=False,
        null=False,
    )
    friendliness = BreedScaleField()
    trainability = BreedScaleField()
    shedding_amount = BreedScaleField()
    exercise_needs = BreedScaleField()

    def __str__(self):
        return self.name


class Dog(models.Model):
    """
    Represents a dog.

    All attributes except for 'favorite_food' and 'favorite_toy'
    are mandatory and not nullable.

    Attributes:
        name (str): Name of the dog.
        age (int): Age of the dog.
        breed (int): Foreign key to Breed.
        gender (str): Gender of the dog.
        color (str): Color of the dog.
        favorite_food (str): Favorite food of the dog.
        favorite_toy (str): Favorite toy of the dog.
    """
    name = models.CharField(
        max_length=CHARFIELD_MAXLENGTH,
        blank=False,
        null=False,
    )
    age = models.PositiveSmallIntegerField(blank=False, null=False)
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    gender = models.CharField(
        max_length=CHARFIELD_MAXLENGTH,
        blank=False,
        null=False,
    )
    color = models.CharField(
        max_length=CHARFIELD_MAXLENGTH,
        blank=False,
        null=False,
    )
    favorite_food = models.CharField(max_length=CHARFIELD_MAXLENGTH)
    favorite_toy = models.CharField(max_length=CHARFIELD_MAXLENGTH)

    def __str__(self):
        return self.name
