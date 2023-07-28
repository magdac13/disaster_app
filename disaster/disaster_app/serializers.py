import django
from .models import Asteroid, NaturalEvent
from rest_framework import serializers

class AsteroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroid
        fields = '__all__'
        
class NaturalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturalEvent
        fields = '__all__'