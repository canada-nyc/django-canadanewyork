from django.contrib import admin

from apps.photos.admin import PhotoInline

from .models import Artist, ArtistPhoto


class ArtistPhotoInline(PhotoInline):
    model = ArtistPhoto

    fields = (
        'position',
        'image',
        ('title', 'date'),
        ('height', 'width', 'depth',),
        'dimensions_text',
        'medium',
        'caption'
    )


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistPhotoInline]
    readonly_fields = ('slug',)
    fieldsets = [
        (None, {
            'fields': ('slug', ('first_name', 'last_name'), 'website', 'visible')
        }),
        ('Resume', {
            'classes': ('full-width',),
            'fields': ('resume_file', 'resume',)
        }),
    ]
    list_display = ('first_name', 'last_name', 'visible')
    list_display_links = ('first_name', 'last_name')
    list_filter = ('visible', )

admin.site.register(Artist, ArtistAdmin)
