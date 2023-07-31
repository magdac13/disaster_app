import django
from .models import Asteroid, NaturalEvent, PossibleScenario, Prediction
from rest_framework import serializers

class AsteroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroid
        fields = '__all__'
        
class NaturalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturalEvent
        fields = '__all__'
        
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'
        
class PossibleScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleScenario
        fields = '__all__'
