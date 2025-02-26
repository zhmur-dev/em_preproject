# Generated by Django 5.1.4 on 2025-01-13 10:40

import django.db.models.deletion
import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, unique=True)),
                ('size', models.CharField(choices=[('tiny', 'Tiny'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], max_length=48)),
                ('friendliness', main.models.BreedScaleField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('trainability', main.models.BreedScaleField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('shedding_amount', main.models.BreedScaleField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('exercise_needs', main.models.BreedScaleField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48)),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(max_length=48)),
                ('color', models.CharField(max_length=48)),
                ('favorite_food', models.CharField(max_length=48)),
                ('favorite_toy', models.CharField(max_length=48)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.breed')),
            ],
        ),
    ]
