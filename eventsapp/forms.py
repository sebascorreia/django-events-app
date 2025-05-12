from .models import Artist, Event, Venue, Tag
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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
        fields = ['name', 'about', 'address', 'email', 'phone', 'website', 'image', 'tags']
    def save(self, commit=True):
        instance = super().save(commit=False)
        geolocator = Nominatim(user_agent = "django_project")
        if self.cleaned_data['address']:
            try:
                location = geolocator.geocode(self.cleaned_data['address'])
                if location:
                    instance.location = f"POINT({location.longitude} {location.latitude})"
                else:
                    raise forms.ValidationError("Address not found. Please enter a valid address.")
            except GeocoderTimedOut:
                raise forms.ValidationError("The geocoding service timed out. Please try again.")
        if commit:
            instance.save()
        return instance
class EventForm(BaseForm):
    tag_type = 'event'

    class Meta:
        model = Event
        fields = ['name', 'date', 'venue', 'artists', 'ticket_price', 'about', 'image', 'tags']

class BaseTagInlineForm(forms.ModelForm):
    existing_tag = forms.ModelChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        label="Choose existing tag"
    )
    new_tag_name = forms.CharField(
        required=False,
        label="Or create new tag",
        max_length=50
    )

    class Meta:
        model = None  # will be set dynamically
        fields = ['existing_tag', 'new_tag_name']
        exclude = ['tag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tag_type = self.tag_type
        self.fields['existing_tag'].queryset = Tag.objects.filter(tag_type=tag_type)
        if self.instance and self.instance.pk:
            self.fields['existing_tag'].initial = self.instance.tag

    def clean(self):
        cleaned_data = super().clean()
        existing = cleaned_data.get('existing_tag')
        new = cleaned_data.get('new_tag_name')

        if not existing and not new:
            raise forms.ValidationError("Please select an existing tag or enter a new one.")
        if existing and new:
            raise forms.ValidationError("Please use either an existing tag or a new one, not both.")
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('existing_tag'):
            self.instance.tag = cleaned_data['existing_tag']
        else:
            tag, _ = Tag.objects.get_or_create(
                name=cleaned_data['new_tag_name'],
                defaults={'tag_type': self.tag_type}
            )
            self.instance.tag = tag
        return super().save(commit=commit)
    
