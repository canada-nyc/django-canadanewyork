from django.contrib import admin

from apps.photos.admin import PhotoInline
from libs.common.admin import editor_form
from .models import Artist


class ArtistAdmin(admin.ModelAdmin):
    form = editor_form(['resume'])
    inlines = [PhotoInline]
    fieldsets = [
        (None, {
            'fields': (('first_name', 'last_name'), 'visible')
        }),
        ('Resume', {
            'classes': ('full-width',),
            'fields': ('resume',)
        }),
    ]
    list_display = ('first_name', 'last_name', 'visible')
    list_display_links = ('first_name', 'last_name')

admin.site.register(Artist, ArtistAdmin)
