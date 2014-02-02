from django.contrib import admin

from apps.photos.admin import photo_inline
from apps.books.admin import BookInline
from libs.common.admin import editor_form

from .models import Artist, ArtistPhoto


class ArtistPhotoInline(photo_inline(ArtistPhoto)):
    fields = (
        ('image', "position"),
        ('title', 'date'),
        ('height', 'width', 'depth',),
        'medium',
        'dimensions_text',
        'caption'
    )


class ArtistAdmin(admin.ModelAdmin):
    form = editor_form(['resume'])
    inlines = [ArtistPhotoInline, BookInline]
    readonly_fields = ('slug',)
    fieldsets = [
        (None, {
            'fields': ('slug', ('first_name', 'last_name'), 'visible')
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
