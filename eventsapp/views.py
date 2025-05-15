from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Artist, Event, Venue
from django.views import generic
from django.conf import settings
from django.utils.html import escape
import json
# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'eventsapp/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events']= Event.objects.all()
        context['artists'] = Artist.objects.all()
        context['venues'] = Venue.objects.all()

        markers = []
        for event in Event.objects.all():
            markers.append({
                "lat": event.venue.location.y,
                "lng": event.venue.location.x,
                "title": escape(event.name),
                "venue": escape(event.venue.name),
                "date": str(event.date),
                "price": float(event.ticket_price)
            })
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY    
        context['events_markers_json'] = json.dumps(markers)
        return context
    
class ArtistDetailView(generic.DetailView):
    model = Artist
    template_name = 'eventsapp/artist.html'
    context_object_name = 'artist'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        artist = self.get_object()
        events = artist.get_events().filter(venue__location__isnull=False)
        
        markers = []
        for event in events:
            markers.append({
                "lat": event.venue.location.y,
                "lng": event.venue.location.x,
                "title": escape(event.name),
                "venue": escape(event.venue.name),
                "date": str(event.date),
                "price": float(event.ticket_price)
            })
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        context['events_markers_json'] = json.dumps(markers)
        return context

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'eventsapp/event.html'
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        return context
class VenueDetailView(generic.DetailView):
    model = Venue
    template_name = 'eventsapp/venue.html'
    context_object_name = 'venue'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        return context

