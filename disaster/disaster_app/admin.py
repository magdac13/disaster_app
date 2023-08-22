from django.contrib import admin
from .models import Asteroid, NaturalEvent
# Register your models here.

admin.site.register(Asteroid)
admin.site.register(NaturalEvent)

