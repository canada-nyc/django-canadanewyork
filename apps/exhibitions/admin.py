from django.contrib import admin


from .models import Exhibition
from apps.photos.admin import PhotoInline


class ExhibitionAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'current')
    fieldsets = (
        (None, {
            'fields': ('name', ('start_date', 'end_date'),)
        }),
        ('Frontpage', {
            'fields': ('current', 'press_release_photo',)
        }),
        ('Related', {
            'fields': ('artists', )
        }),
    )
admin.site.register(Exhibition, ExhibitionAdmin)
