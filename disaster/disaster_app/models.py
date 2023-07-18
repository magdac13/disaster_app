from django.db import models

# Create your models here.


class Asteroid(models.Model):
    name = models.CharField(max_length=100)
    diameter = models.FloatField()
    is_hazardous = models.BooleanField()
    velocity = models.FloatField()
    orbiting_body = models.CharField(max_length=100)
    close_approach_date = models.DateField()
    miss_distance = models.FloatField()



