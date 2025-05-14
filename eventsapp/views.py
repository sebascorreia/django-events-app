from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Artist, Event, Venue
from django.views import generic
# Create your views here.


def home(request):
    return render(request, 'eventsapp/home.html')
class ArtistDetailView(generic.DetailView):
    model = Artist
    template_name = 'eventsapp/artist.html'
    context_object_name = 'artist'
class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'eventsapp/event.html'
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.conf import settings
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        return context
class VenueDetailView(generic.DetailView):
    model = Venue
    template_name = 'eventsapp/venue.html'
    context_object_name = 'venue'

