from django.db import models
from django.contrib.gis.db import models as gis_models
# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = gis_models.PointField()