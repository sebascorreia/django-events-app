from django.contrib import admin
from .models import Artist, Event, Venue, Tag, ArtistTag, EventTag, VenueTag, Schedule
from .forms import ArtistForm, VenueForm, EventForm, BaseTagInlineForm

# Register your models here.
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = ['artist', 'info', 'time']
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
    inlines = [EventTagInline, ScheduleInline]
    list_display = ('name', 'date', 'venue',)
    search_fields = ('name', 'venue__name', 'tags__name',)
    filter_horizontal = ('artists',)
    autocomplete_fields = ['venue']



admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_type')
    search_fields = ('name',)
    list_filter = ('tag_type',)
