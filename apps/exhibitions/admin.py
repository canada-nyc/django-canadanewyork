from django.contrib import admin


from apps.photos.admin import PhotoInline
from libs.common.admin import editor_form
from .models import Exhibition


class ExhibitionAdmin(admin.ModelAdmin):
    form = editor_form(['description'])
    inlines = [PhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'current')
    fieldsets = (
        (None, {
            'fields': ('name', ('start_date', 'end_date'), 'artists',)
        }),
        ('Homepage', {
            'fields': (('current', 'press_release_photo',), 'description',)
        }),
    )
    raw_id_fields = ('artists',)
    autocomplete_lookup_fields = {
        'm2m': ['artists'],
    }

admin.site.register(Exhibition, ExhibitionAdmin)
