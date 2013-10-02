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
            'fields': (
                'title',
                ('date', 'date_text'),
                'publisher',
                ('author_first_name', 'author_last_name'),
                'pages_range',
            ),
        }),
        ('Article', {
            'classes': ('full-width',),
            'fields': ('content', 'content_file',)
        }),
        ('Related to', {
            'fields': ('exhibition', 'artist')
        }),
    )

    raw_id_fields = ('artist', 'exhibition')
    autocomplete_lookup_fields = {
        'fk': ['artist', 'exhibition'],
    }

admin.site.register(Press, PressAdmin)
