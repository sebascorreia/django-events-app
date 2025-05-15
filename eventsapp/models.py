from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from geopy.geocoders import Nominatim
# Create your models here.
class Tag(models.Model):
    TAG_TYPES = [
        ('artist', 'Artist'),
        ('event', 'Event'),
        ('venue', 'Venue'),
    ]
    name= models.CharField(max_length=50, unique=True)
    tag_type = models.CharField(max_length=10, choices=TAG_TYPES, default='event')
    def __str__(self):
        return self.name
    

class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = gis_models.PointField(null =True, blank=True)
    about = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='venue_images/', blank=True)
    tags = models.ManyToManyField(Tag, related_name='venues', through='VenueTag', blank=True)
    
    def get_tags(self):
        return ", ".join(tag.name for tag in self.tags.all())
    def get_events(self):
        return self.events.all()
    def get_city(self):
        if self.location:
            geolocator =Nominatim(user_agent="eventsapp")
            location = geolocator.reverse((self.location.y, self.location.x))
            return location.raw.get('address', {}).get('city')
        return None
    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='artist_images/', blank=True)
    tags= models.ManyToManyField(Tag, related_name='artists', through= 'ArtistTag', blank=True)
    def __str__(self):
        return self.name
    def get_tags(self):
        return ", ".join(tag.name for tag in self.tags.all())
    def get_events(self):
        return self.events.all()
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    artists = models.ManyToManyField(Artist, related_name='events', blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True)
    tags = models.ManyToManyField(Tag, related_name='events', through='EventTag', blank=True)
    def __str__(self):
        return self.name
    def get_tags(self):
        return ", ".join(tag.name for tag in self.tags.all())
    def get_artists(self):
        return self.artists.all()
    def get_artist_tags(self):
        artist_tags = []
        for artist in self.artists.all():
            artist_tags.extend(artist.tags.all())
        return artist_tags
    def get_all_tags(self):
        all_tags = set(self.tags.all())
        all_tags.update(self.get_artist_tags())
        return all_tags
    def get_schedule(self):
        return self.schedules.all()
class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, blank = True, null=True, related_name='schedules')
    info = models.TextField(blank=True, null=True)
    time= models.TimeField()
    # if both artist and info are deleted then the schedule entry should be deleted
    # make sure either artist or info is provided
    def clean(self):
        if not self.artist and not self.info:
            raise ValidationError("Either artist or info must be provided.")
        if self.artist and self.info:
            raise ValidationError("Please only provide either artist or info,")
    def __str__(self):
        if self.artist:
            return f"{self.artist.name} at {self.time} for {self.event.name}"
        elif self.info:
            return f"{self.info} at {self.time} for {self.event.name}"
        return f"Schedule entry at {self.time} for {self.event.name}"
    
class ArtistTag(models.Model):
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
class EventTag(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
class VenueTag(models.Model):
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
