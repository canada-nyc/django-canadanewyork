from django.contrib import admin

from libs.common.admin import editor_form
from .models import Press


class PressAdmin(admin.ModelAdmin):
    form = editor_form(['content'])
    date_hierarchy = 'date'
    list_display = ('title', 'publisher', 'author_last_name', 'date', 'exhibition', 'artist')
    list_filter = ('publisher', 'date', 'exhibition', 'artist')

    fieldsets = (
        (None, {
            'fields': ('title', 'date', ('publisher', 'author_first_name', 'author_last_name'))
        }),
        ('Article', {
            'classes': ('full-width',),
            'fields': ('content', 'content_file',)
        }),
        ('Related', {
            'fields': ('exhibition', 'artist')
        }),
    )

admin.site.register(Press, PressAdmin)
