from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("artist/<int:pk>/", views.ArtistDetailView.as_view(), name="artist_detail"),
    path("venue/<int:pk>/", views.VenueDetailView.as_view(), name="venue_detail"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)