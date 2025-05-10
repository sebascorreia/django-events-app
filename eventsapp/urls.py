from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("artist/<int:artist_id>/", views.artist_detail, name="artist_detail"),
]