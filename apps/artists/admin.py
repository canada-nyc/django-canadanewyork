from django.contrib import admin

from apps.photos.admin import photo_inline
from apps.books.admin import BookInline
from libs.common.admin import editor_form

from .models import Artist, ArtistPhoto


class ArtistPhotoInline(photo_inline(ArtistPhoto)):
    fields = (
        ('image', "position"),
        ('title', 'year'),
        ('height', 'width', 'depth',),
        'dimensions_text',
        'medium',
        'caption'
    )


class ArtistAdmin(admin.ModelAdmin):
    form = editor_form(['resume'])
    inlines = [ArtistPhotoInline, BookInline]
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
    list_filter = ('visible', )

admin.site.register(Artist, ArtistAdmin)
