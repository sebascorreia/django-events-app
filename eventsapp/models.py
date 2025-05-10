from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class Tag(models.Model):
    name= models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = gis_models.PointField()
    about = models.TextField()
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField()
    image = models.ImageField(upload_to='venue_images/')
    tags = models.ManyToManyField(Tag, related_name='venues', blank=True)
    
    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    image = models.ImageField(upload_to='artist_images/')
    tags= models.ManyToManyField(Tag, related_name='artists', blank=True)
    def __str__(self):
        return self.name
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist, related_name='events', blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_images/')
    tags = models.ManyToManyField(Tag, related_name='events', blank=True)
    schedule = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.name
class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, blank = True, null=True, related_name='schedules')
    info = models.TextField(blank=True, null=True)
    time= models.TimeField()
    # if both artist and info are deleted then the schedule entry should be deleted
    # make sure either artist or info is provided
    
    def __str__(self):
        if self.artist:
            return f"{self.artist.name} at {self.time} for {self.event.name}"
        elif self.info:
            return f"{self.info} at {self.time} for {self.event.name}"
        return f"Schedule entry at {self.time} for {self.event.name}"