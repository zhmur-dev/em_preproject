from django.contrib import admin

from .models import Breed, Dog


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'size', 'friendliness',
        'trainability', 'shedding_amount', 'exercise_needs'
    )
    list_editable = (
        'name', 'size', 'friendliness',
        'trainability', 'shedding_amount', 'exercise_needs'
    )
    list_filter = (
        'size', 'friendliness', 'trainability',
        'shedding_amount', 'exercise_needs'
    )


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'age', 'breed', 'gender', 'color',
        'favorite_food', 'favorite_toy'
    )
    list_editable = (
        'name', 'age', 'breed', 'gender', 'color',
        'favorite_food', 'favorite_toy'
    )
    list_filter = (
        'breed', 'color', 'gender', 'age',
    )
    search_fields = ('name',)
