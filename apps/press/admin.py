from django.contrib import admin

from libs.common.admin import editor_form
from .models import Press


class PressAdmin(admin.ModelAdmin):
    form = editor_form(['content'])
    date_hierarchy = 'date'
    list_display = ('__unicode__', 'publisher', 'date', 'exhibition', 'artist')
    llist_filter = ('publisher', 'date', 'exhibition', 'artist')

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'publisher', 'link')
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
