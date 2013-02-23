from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Exhibition
from apps.photos.admin import PhotoInline


class ExhibitionAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [PhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'current')
    fields = ('name', 'description', ('current', 'press_release_photo'), ('start_date', 'end_date'), 'artists',)

admin.site.register(Exhibition, ExhibitionAdmin)
