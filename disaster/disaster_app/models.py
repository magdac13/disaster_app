from django.contrib.gis.db import models
from django.db.models import Min
from .managers import AsteroidManager, NaturalEventManager


# Create your models here.


class Asteroid(models.Model):
    name = models.CharField(max_length=100)
    diameter = models.FloatField()
    is_hazardous = models.BooleanField()
    velocity = models.FloatField()
    orbiting_body = models.CharField(max_length=100)
    close_approach_date = models.DateField()
    miss_distance = models.FloatField()

    objects = AsteroidManager()

    @staticmethod
    def remove_duplicates():
        duplicate_names = (
            Asteroid.objects.values('name')
            .annotate(min_id=Min('id'))
            .values_list('name', 'min_id')
        )

        Asteroid.objects.exclude(id__in=[min_id for name, min_id in duplicate_names]).delete()


class NaturalEvent(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    geo_location = models.PointField()

    objects = NaturalEventManager()







