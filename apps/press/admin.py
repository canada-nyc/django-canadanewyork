from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition', 'slug')

    fields = (('title', 'date'), ('publisher', 'author'), 'image', 'link', 'old_path')

admin.site.register(Press, PressAdmin)
