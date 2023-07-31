from django.contrib.gis.db import models
from django.db.models import Min
from .managers import AsteroidManager, NaturalEventManager
from django.contrib.auth.models import User


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
    
    def __str__(self):
        return self.name, self.orbiting_body

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

    def __str__(self):
        return self.title, self.category
    
    @staticmethod
    def remove_duplicates():
        duplicate_titles = (
            NaturalEvent.objects.values('title')
            .annotate(min_id=Min('id'))
            .values_list('title', 'min_id')
        )

        NaturalEvent.objects.exclude(id__in=[min_id for title, min_id in duplicate_titles]).delete()


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE)
    natural_event = models.ForeignKey(NaturalEvent, on_delete=models.CASCADE)
    asteroid_result = models.JSONField()
    natural_event_result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class PossibleScenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE)
    natural_event = models.ForeignKey(NaturalEvent, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    scenario = models.JSONField()
    
    
    


    


