import json
import random

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.const import BREED_SCALE, BREED_SIZES
from main.models import Breed


TEST_BREEDS = [
    'German Shepherd', 'Bulldog', 'Labrador Retriever', 'French Bulldog',
    'Golden Retriever', 'Siberian Husky', 'Beagle', 'Alaskan Malamute',
    'Poodle', 'Chihuahua', 'Australian Cattle Dog', 'Dachshund'
]
TEST_NAMES = [
    'Luna', 'Bella', 'Charlie', 'Lucy', 'Daisy', 'Cooper', 'Bailey', 'Max'
]
TEST_GENDERS = ['M', 'F']
TEST_COLORS = [
    'black', 'white/cream', 'brown', 'red',
    'golden/yellow/cream', 'gray/silver/blue'
]
TEST_FOOD = ['beef', 'pork', 'chicken', 'lamb']
TEST_TOYS = ['plush toys', 'squeaky toys', 'puzzle toys', 'hard chew toys']


class BreedsApiTestCase(APITestCase):
    def test_post(self):
        print ('\nTest: POST /api/breeds/')
        url = reverse('breed-list')
        for i in range(len(TEST_BREEDS)):
            data = {
                'name': TEST_BREEDS[i],
                'size': (random.choice(BREED_SIZES))[0],
                'friendliness': (random.choice(BREED_SCALE))[0],
                'trainability': (random.choice(BREED_SCALE))[0],
                'shedding_amount': (random.choice(BREED_SCALE))[0],
                'exercise_needs': (random.choice(BREED_SCALE))[0]
            }
            json_data = json.dumps(data)
            response = self.client.post(
                url, data=json_data, content_type='application/json'
            )
            print(response.data)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class DogsApiTestCase(APITestCase):
    def test_post(self):
        print('\nTest: POST /api/dogs/')
        breed = Breed.objects.create(
            name = random.choice(TEST_BREEDS),
            size = (random.choice(BREED_SIZES))[0],
            friendliness = (random.choice(BREED_SCALE))[0],
            trainability = (random.choice(BREED_SCALE))[0],
            shedding_amount = (random.choice(BREED_SCALE))[0],
            exercise_needs = (random.choice(BREED_SCALE))[0],
        )
        url = reverse('dog-list')
        for i in range(len(TEST_NAMES)):
            data = {
                'name': TEST_NAMES[i],
                'breed': breed.id,
                'age': random.choice(range(13)),
                'gender': random.choice(TEST_GENDERS),
                'color': random.choice(TEST_COLORS),
                'favorite_food': random.choice(TEST_FOOD),
                'favorite_toy': random.choice(TEST_TOYS)
            }
            json_data = json.dumps(data)
            response = self.client.post(
                url, data=json_data, content_type='application/json'
            )
            print(response.data)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)
