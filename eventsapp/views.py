from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Artist, Event, Venue
# Create your views here.


def home(request):
    return render(request, 'eventsapp/home.html')

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    return render(request, 'eventsapp/artist.html', {'artist': artist})
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'eventsapp/event.html', {'event': event})
def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return render(request, 'eventsapp/venue.html', {'venue': venue})

