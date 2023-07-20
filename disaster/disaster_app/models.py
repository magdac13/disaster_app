import os

import requests
from django.contrib.auth.models import User, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.contrib.gis.db import models

from dotenv import load_dotenv

# Create your models here.


class AsteroidManager(models.Manager):

    def __init__(self):

        super().__init__()
        self.__load_env()
        self.load_and_save_to_db()
        self.get_data_from_api()
        return

    def __load_env(self):
        load_dotenv()
        self.__env = {
            'nasa_api_key': os.getenv('NASA_API_KEY'),
            'input_url': os.getenv('INPUT_URL'),
        }
        return

    def load_and_save_to_db(self):
        data = self.get_data_from_api()
        self.save_to_db(data)

    def get_data_from_api(self):
        input_url = self.__env.get('input_url')
        nasa_api_key = self.__env.get('nasa_api_key')
        url = input_url.format(api_key=nasa_api_key)
        response = requests.get(url)
        data_json = response.json()
        return data_json

    def save_to_db(self, data):
        asteroids = []
        for asteroid_data in data.get('near_earth_objects', []):
            close_approach_data = asteroid_data.get('close_approach_data', [])[0]

            asteroid = Asteroid(
                name=asteroid_data.get('name'),
                diameter=asteroid_data.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max'),
                is_hazardous=asteroid_data.get('is_potentially_hazardous_asteroid'),
                velocity=close_approach_data.get('relative_velocity', {}).get('kilometers_per_hour'),
                orbiting_body=close_approach_data.get('orbiting_body'),
                close_approach_date=datetime.strptime(close_approach_data.get('close_approach_date'), '%Y-%m-%d'),
                miss_distance=close_approach_data.get('miss_distance', {}).get('kilometers')
            )
            asteroids.append(asteroid)

        Asteroid.objects.bulk_create(asteroids)

# class AsteroidManager(models.Manager):
#
#     def __init__(self):
#         super().__init__()
#         self.__load_env()
#         self.__get_queryset()
#         self.__save_to_db()
#         return
#
#     def __load_env(self):
#         load_dotenv()
#         self.__env = {
#             'nasa_api_key': os.getenv('NASA_API_KEY'),
#             'input_url': os.getenv('INPUT_URL'),
#         }
#         return
#
#     def __get_queryset(self):
#         input_url = self.__env.get('input_url')
#         nasa_api_key = self.__env.get('nasa_api_key')
#         url = input_url.format(api_key=nasa_api_key)
#         response = requests.get(url)
#         data = response.json()
#         self.__save_to_db(data)
#         return
#
#     def __save_to_db(self, data):
#         asteroids = []
#         for asteroid_data in data.get('near_earth_objects', []):
#             close_approach_data = asteroid_data.get('close_approach_data', [])[0]
#
#             asteroid = Asteroid(
#                 name=asteroid_data.get('name'),
#                 diameter=asteroid_data.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max'),
#                 is_hazardous=asteroid_data.get('is_potentially_hazardous_asteroid'),
#                 velocity=close_approach_data.get('relative_velocity', {}).get('kilometers_per_hour'),
#                 orbiting_body=close_approach_data.get('orbiting_body'),
#                 close_approach_date=datetime.strptime(close_approach_data.get('close_approach_date'), '%Y-%m-%d'),
#                 miss_distance=close_approach_data.get('miss_distance', {}).get('kilometers'),
#             )
#             asteroids.append(asteroid)
#
#         Asteroid.objects.bulk_create(asteroids)
#         return


class Asteroid(models.Model):
    name = models.CharField(max_length=100)
    diameter = models.FloatField()
    is_hazardous = models.BooleanField()
    velocity = models.FloatField()
    orbiting_body = models.CharField(max_length=100)
    close_approach_date = models.DateField()
    miss_distance = models.FloatField()


class NaturalEvent(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    geo_location = models.PointField()





