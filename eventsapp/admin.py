from django.contrib import admin
from .models import Artist, Event, Venue, Tag, ArtistTag, EventTag, VenueTag
from .forms import ArtistForm, VenueForm, EventForm
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models.signals import m2m_changed
from django import forms

# Register your models here.
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

class BaseTagInline(admin.StackedInline):
    extra = 1
    tag_type = None
    model = None  # Set in subclasses

    def get_formset(self, request, obj=None, **kwargs):
        # Dynamically create a form class with proper Meta including correct model
        form_class = type(
            f"{self.tag_type.capitalize()}TagInlineForm",
            (BaseTagInlineForm,),
            {
                "tag_type": self.tag_type,
                "Meta": type("Meta", (), {
                    "model": self.model,
                    "fields": ['existing_tag', 'new_tag_name'],
                    "exclude": ['tag'],
                }),
            }
        )
        kwargs['form'] = form_class
        return super().get_formset(request, obj, **kwargs)
    
class ArtistTagInline(BaseTagInline):
    model = ArtistTag
    tag_type = 'artist'

class VenueTagInline(BaseTagInline):
    model = VenueTag
    tag_type = 'venue'

class EventTagInline(BaseTagInline):
    model = EventTag
    tag_type = 'event'

class ArtistAdmin(admin.ModelAdmin):
    form  = ArtistForm
    inlines = [ArtistTagInline]
    list_display = ('name',)
    search_fields = ('name', 'tags__name',)

class VenueAdmin(admin.ModelAdmin):
    form= VenueForm
    inlines = [VenueTagInline]
    list_display = ('name', 'address', 'email',)
    search_fields = ('name', 'tags__name',)


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    inlines = [EventTagInline]
    list_display = ('name', 'date', 'venue',)
    search_fields = ('name', 'venue__name', 'tags__name',)

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_type')
    search_fields = ('name',)
    list_filter = ('tag_type',)
