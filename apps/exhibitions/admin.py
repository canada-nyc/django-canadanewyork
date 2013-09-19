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
        'dimensions_text',
        'medium',
        'caption'
    )


class ExhibitionAdmin(admin.ModelAdmin):
    form = editor_form(['description', 'extra_info'])
    inlines = [ExhibitionPhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'current')
    list_filter = ('current', )
    fieldsets = (
        (None, {
            'fields': ('name', ('start_date', 'end_date'), 'artists', 'description',)
        }),
        ('Homepage', {
            'fields': (('current', 'press_release_photo',), 'extra_info',)
        }),
    )

    raw_id_fields = ('artists',)
    autocomplete_lookup_fields = {
        'm2m': ['artists'],
    }

admin.site.register(Exhibition, ExhibitionAdmin)
