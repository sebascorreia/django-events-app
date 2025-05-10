from .models import Artist, Event, Venue, Tag
from django import forms
from django.urls import reverse
from django.utils.html import format_html

class BaseForm(forms.ModelForm):
    tag_type = None
class ArtistForm(BaseForm):
    tag_type = 'artist'
    class Meta:
        model = Artist
        fields = ['name', 'about', 'image', 'tags']
        
class VenueForm(BaseForm):
    tag_type = 'venue'
    class Meta:
        model = Venue
        fields = ['name', 'location', 'about', 'address', 'email', 'phone', 'website', 'image', 'tags']

class EventForm(BaseForm):
    tag_type = 'event'

    class Meta:
        model = Event
        fields = ['name', 'date', 'venue', 'artists', 'ticket_price', 'about', 'image', 'tags', 'schedule']