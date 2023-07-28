from django.db import models
from datetime import datetime, timedelta
from django.contrib.gis.geos import Point
import requests
import os


class AsteroidManager(models.Manager):
    """ Manager for Asteroid model """

    def get_data_from_api(self):
        api_key = os.getenv('NASA_API_KEY')
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}&size=50&is_potentially_hazardous=true'

        response = requests.get(url)
        return response.json()

    def save_data_to_db(self, data):
        unique_asteroids = set()
        near_earth_objects = data.get('near_earth_objects', [])

        for date, asteroids_data in near_earth_objects.items():
            for asteroid_data in asteroids_data:
                asteroid_id = asteroid_data.get('id') if isinstance(asteroid_data, dict) else asteroid_data
                if asteroid_id not in unique_asteroids:
                    unique_asteroids.add(asteroid_id)

                    close_approach_data = asteroid_data.get('close_approach_data', [{}])[0]

                    asteroid_object = self.model(
                        name=asteroid_data.get('name'),
                        diameter=asteroid_data.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max'),
                        is_hazardous=asteroid_data.get('is_potentially_hazardous_asteroid'),
                        velocity=close_approach_data.get('relative_velocity', {}).get('kilometers_per_hour'),
                        orbiting_body=close_approach_data.get('orbiting_body'),
                        close_approach_date=datetime.strptime(close_approach_data.get('close_approach_date'), '%Y-%m-%d'),
                        miss_distance=close_approach_data.get('miss_distance', {}).get('kilometers')
                    )

                    asteroid_object.save()


class NaturalEventManager(models.Manager):
    """ Manager for NaturalEvents model """

    def get_data_from_api(self):

        url = os.getenv('INPUT_URL')

        response = requests.get(url)
        return response.json()

    def save_data_to_db(self, data):
        unique_events = set()
        events_data = data.get('events', [])

        for event_data in events_data:
            event_id = event_data.get('id')
            if event_id not in unique_events:
                unique_events.add(event_id)

                geometry_data = event_data.get('geometries', [])[0]
                coordinates = geometry_data.get('coordinates')
                point = Point(coordinates[0], coordinates[1])

                natural_event_object = self.model(
                    title=event_data.get('title'),
                    category=event_data.get('categories', [])[0].get('title'),
                    date=geometry_data.get('date'),
                    geo_location=point
                )

                natural_event_object.save()
