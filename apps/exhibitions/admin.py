from django.contrib import admin


from apps.photos.admin import photo_inline
from libs.common.admin import editor_form
from .models import Exhibition, ExhibitionPhoto


class ExhibitionPhotoInline(photo_inline(ExhibitionPhoto)):
    fields = (
        ('image', "position"),
        'artist_text',
        ('title', 'date'),
        ('height', 'width', 'depth',),
        'medium',
        'dimensions_text',
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
    form = editor_form(['description', 'extra_info'])
    readonly_fields = ('slug',)

    raw_id_fields = ('artists',)
    autocomplete_lookup_fields = {
        'm2m': ['artists'],
    }

admin.site.register(Exhibition, ExhibitionAdmin)
