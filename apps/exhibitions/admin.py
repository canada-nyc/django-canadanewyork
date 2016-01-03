import autocomplete_light

from django.contrib import admin

from apps.photos.admin import PhotoInline
from .models import Exhibition, ExhibitionPhoto


class ExhibitionPhotoInline(PhotoInline):
    model = ExhibitionPhoto
    fields = (
        'position',
        'image',
        'artist_text',
        ('title', 'date'),
        ('height', 'width', 'depth',),
        'dimensions_text',
        'medium',
        'caption'
    )


class ExhibitionAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'current')
    list_filter = ('current', )

    fieldsets = (
        (None, {
            'fields': (
                'slug',
                'name',
                ('start_date', 'end_date'),
                'artists',
                'description',
            )
        }),
        ('Homepage', {
            'fields': (('current', 'press_release_photo',), 'extra_info',)
        }),
    )
    inlines = [ExhibitionPhotoInline]
    readonly_fields = ('slug',)

    form = autocomplete_light.modelform_factory(Exhibition, fields='__all__')


admin.site.register(Exhibition, ExhibitionAdmin)
