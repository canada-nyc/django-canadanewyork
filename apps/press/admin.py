from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('title', 'publisher', 'author', 'date', 'exhibition', 'artist')
    list_filter = ('publisher', 'date', 'exhibition', 'artist')
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {
            'fields': (
                'slug',
                'title',
                ('date', 'date_text'),
                'publisher',
                'author',
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
