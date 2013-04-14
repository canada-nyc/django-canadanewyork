from django.contrib import admin

from .models import Artist
from apps.photos.admin import PhotoInline


class ArtistAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    fields = (('first_name', 'last_name'), 'visible',)
    list_display = ('first_name', 'last_name', 'visible')
    list_display_links = ('first_name', 'last_name')

admin.site.register(Artist, ArtistAdmin)
