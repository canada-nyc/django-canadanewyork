from django.contrib import admin

from .models import Artist
from ..common.admin import PhotoInline


class ArtistAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    fields = (('first_name', 'last_name'), 'resume',)
    list_display = ('first_name', 'last_name', 'visible')


admin.site.register(Artist, ArtistAdmin)
